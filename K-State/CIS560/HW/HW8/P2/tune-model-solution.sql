-- CIS560 assignment 7 sample solution.  

create index DoctorSpecialty on Doctor(specialty);
----useful for the query that has specialty in the WHERE clause

create index DoctorNameIndex on Doctor(fname,lname);
----queries related to doctors involve both fname and lname
----separate indexes on fname or lname would not help that much

create index PatientNameIndex on Patient(fname,lname);
----same argument as for the DoctorNameIndex

create index DiseaseIndex ON Disease(disease); 
----useful for the query on disease

create index PatientAgeIndex ON Patient(age);
----we have a range query over age, so it's useful to create an index for age; 
----cluster PatientAgeIndex, if possible

create index PatientZipcodeIndex ON Patient(zipcode); 
----useful for the query that has zipcode in the WHERE clause