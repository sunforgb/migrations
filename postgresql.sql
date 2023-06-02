create type employee_type as ENUM ('employee', 'analyst', 'department_dir', 'admin');

alter table api_myuser alter user_type type employee_type USING user_type::employee_type;

select column_name, data_type from information_schema.columns where table_name='api_myuser';

create extension plpython3u;

create role employee WITH LOGIN;
GRANT SELECT ON api_citizenship to employee;
GRANT SELECT ON api_department to employee;
GRANT SELECT ON api_doc_migr_pers to employee;
GRANT SELECT ON api_migrant to employee;
GRANT SELECT ON api_myuser to employee;
GRANT SELECT ON api_myuser_department to employee;
GRANT SELECT ON api_phone to employee;
GRANT SELECT ON api_registration_statement to employee;
GRANT SELECT ON api_unregistration_statement to employee;

GRANT update ON api_registration_statement to employee;
GRANT update ON api_unregistration_statement to employee;

CREATE ROLE department_dir WITH LOGIN INHERIT;
GRANT employee to department_dir;
GRANT SELECT ON api_employee to department_dir;
GRANT INSERT ON api_migrant to department_dir;
GRANT INSERT ON api_phone to department_dir;
GRANT INSERT ON api_doc_migr_pers to department_dir;
GRANT UPDATE ON api_registration_statement to department_dir;
GRANT UPDATE ON api_unregistration_statement to department_dir;
GRANT INSERT ON api_registration_statement to department_dir;
GRANT INSERT ON api_unregistration_statement to department_dir;

create role analyst WITH LOGIN;
GRANT SELECT ON api_citizenship to analyst;
GRANT SELECT ON api_department to analyst;
GRANT SELECT ON api_doc_migr_pers to analyst;
GRANT SELECT ON api_employee to analyst;
GRANT SELECT ON api_migrant to analyst;
GRANT SELECT ON api_myuser to analyst;
GRANT SELECT ON api_myuser_department to analyst;
GRANT SELECT ON api_phone to analyst;
GRANT SELECT ON api_registration_statement to analyst;
GRANT SELECT ON api_unregistration_statement to analyst;



                    List of relations
 Schema |             Name             | Type  |  Owner   
--------+------------------------------+-------+----------
 public | api_citizenship              | table | postgres
 public | api_department               | table | postgres
 public | api_doc_migr_pers            | table | postgres
 public | api_employee                 | table | postgres
 public | api_migrant                  | table | postgres
 public | api_myuser                   | table | postgres
 public | api_myuser_department        | table | postgres
 public | api_myuser_groups            | table | postgres
 public | api_myuser_user_permissions  | table | postgres
 public | api_phone                    | table | postgres
 public | api_registration_statement   | table | postgres
 public | api_unregistration_statement | table | postgres
 public | auth_group                   | table | postgres
 public | auth_group_permissions       | table | postgres
 public | auth_permission              | table | postgres
 public | django_admin_log             | table | postgres
 public | django_content_type          | table | postgres
 public | django_migrations            | table | postgres
 public | django_session               | table | postgres


CREATE FUNCTION create_new_department_dir() RETURNS TRIGGER AS $create_new_department_dir$
    BEGIN
        EXECUTE format('CREATE ROLE department_dir_%s WITH LOGIN INHERIT', NEW.id);
        EXECUTE format('GRANT department_dir TO department_dir_%s', NEW.id);
        RETURN NEW;
    END;
$create_new_department_dir$ LANGUAGE plpgsql;

CREATE TRIGGER create_new_department_dir
AFTER INSERT ON api_myuser
FOR EACH ROW
WHEN (NEW.user_type = 'department_dir')
EXECUTE FUNCTION create_new_department_dir();

CREATE FUNCTION delete_department_dir() RETURNS TRIGGER AS $delete_department_dir$
    BEGIN
        EXECUTE format('DROP ROLE department_dir_%s', OLD.id);
        RETURN OLD;
    END;
$delete_department_dir$ LANGUAGE plpgsql;

CREATE TRIGGER delete_department_dir
BEFORE DELETE ON api_myuser
FOR EACH ROW
WHEN(OLD.user_type = 'department_dir')
EXECUTE FUNCTION delete_department_dir();

CREATE FUNCTION create_new_employee() RETURNS TRIGGER as $create_new_employee$
    BEGIN
        EXECUTE format('CREATE ROLE employee_%s WITH LOGIN INHERIT', NEW.id);
        EXECUTE format('GRANT employee to employee_%s', NEW.id);
        RETURN NEW;
    END;
$create_new_employee$ LANGUAGE plpgsql;

CREATE TRIGGER create_new_employee
AFTER INSERT ON api_myuser
FOR EACH ROW
WHEN (NEW.user_type = 'employee')
EXECUTE FUNCTION create_new_employee();

CREATE FUNCTION delete_employee() RETURNS TRIGGER AS $delete_employee$
    BEGIN
        EXECUTE format('DROP ROLE employee_%s', OLD.id);
        RETURN OLD;
    END;
$delete_employee$ LANGUAGE plpgsql;

CREATE TRIGGER delete_employee
BEFORE DELETE ON api_myuser
FOR EACH ROW
WHEN(OLD.user_type = 'employee')
EXECUTE FUNCTION delete_employee();


alter table api_registration_statement enable row level security;

CREATE POLICY employee_registr_state ON api_registration_statement
AS PERMISSIVE
USING (department_id IN (
    select department_id from api_myuser_department
    WHERE (substring(current_user from '[0-9]+') = myuser_id::text)
) OR (
    current_user LIKE 'analyst'
));

alter table api_unregistration_statement enable row level security;

CREATE POLICY employee_unregistr_state ON api_unregistration_statement
AS PERMISSIVE
USING (department_id IN (
    select department_id from api_myuser_department
    WHERE (substring(current_user from '[0-9]+') = myuser_id::text)
) OR (
    current_user LIKE 'analyst'
));

CREATE VIEW reg_state AS SELECT address, number, count(person_id) 
FROM api_registration_statement
JOIN api_department ON (department_id = api_department.id)
JOIN api_phone ON (api_department.contact_id = api_phone.id)
group by address, number;


create or replace procedure report_registration_statement()
LANGUAGE plpgsql
AS $$
BEGIN
    execute format('COPY (SELECT * FROM reg_state) TO %L CSV HEADER DELIMITER %L', '/tmp/reg_state_report.csv', '|');
END $$;