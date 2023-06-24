

DATA travel;
	INFILE "/home/u63359312/Proiect/Travel.csv" DSD;
	INPUT Destination $ Start_date $ End_date $ Traveler_name $ Traveler_age Traveler_gender $ Traveler_nationality $ 
	Accommodation_type $ Accommodation_cost;
format Accommodation_cost dollar.;
RUN;

PROC PRINT DATA = travel;
run;

PROC FORMAT;
VALUE $Traveler_gender 'Male'='M'
				other='F';
RUN;

PROC PRINT DATA = travel;
FORMAT Traveler_gender $Traveler_gender.;
RUN;

PROC FORMAT;
VALUE Accommodation_cost  low-2000='Low cost'
				2001-4000='Medium cost'
				4001-high='High cost';
RUN;

PROC PRINT DATA = travel;
FORMAT Accommodation_cost Accommodation_cost.;
RUN;

PROC PRINT DATA=WORK.TRAVEL;
WHERE Traveler_nationality EQ 'American' AND Traveler_gender="Male";
RUN;

/*Afiseaza calatorii care au peste 40 de ani*/
PROC PRINT DATA=WORK.TRAVEL;
WHERE Traveler_age GT 40;
VAR Destination Traveler_name Traveler_age Accommodation_type Accommodation_cost;
FORMAT Accommodation_cost Accommodation_cost.;
RUN;

/* exemplu libname*/
libname lib1 '/home/u63359312/Proiect';
Data lib1.travel;
INFILE "/home/u63359312/Proiect/Travel.csv" DSD;
	INPUT Destination $ Start_date $ End_date $ Traveler_name $ Traveler_age Traveler_gender $ Traveler_nationality $ 
	Accommodation_type $ Accommodation_cost;
format Accommodation_cost dollar.;
RUN;

/* Frecventa de aparitie pentru destinatii */
TITLE "Frecventa de aparitie pentru destinatii";
PROC FREQ DATA=lib1.travel;
		TABLES Destination /NOCUM NOPERCENT;
RUN;

DATA discount;
infile '/home/u63359312/Proiect/Travel.csv' dsd;
INPUT Destination $ Start_date $ End_date $ Traveler_name $ Traveler_age Traveler_gender $ Traveler_nationality $ 
	Accommodation_type $ Accommodation_cost;
SELECT;
	WHEN (Traveler_age le 25) Discount=0.17 ;	
	WHEN (Traveler_age ge 45) Discount=0.1 ;
	OTHERWISE Discount=0.2 ;
END;
RUN;

PROC PRINT DATA=discount;
VAR Traveler_name Traveler_age Discount;
run;

DATA pret_nou;
set discount;
do
Pret_Nou=Accommodation_cost-Discount*Accommodation_cost;
end;
run;

proc print data=pret_nou;
var Accommodation_cost Discount Pret_Nou;
run;

data hotel;
set pret_nou;
where Accommodation_type like 'H%';
RUN;
proc print data=hotel;
var Accommodation_type Pret_Nou;
run;

data durata;
INFILE "/home/u63359312/Proiect/Travel.csv" DSD;
INPUT Destination $ Start_date:mmddyy.  End_date:mmddyy. Traveler_name $ Traveler_age Traveler_gender $ Traveler_nationality $ 
	Accommodation_type $ Accommodation_cost;
do
durata_zile=intck('day',Start_date,End_date);
end;
run;

proc print data=durata;
run;

data calatori;
set durata (KEEP=Traveler_name Traveler_age Accommodation_cost durata_zile);
if Traveler_age ge 30 then
	i=0;
	Total=0;
	do while(i lt durata_zile);
	Total=Accommodation_cost + Total;
	i+1;
	end;
RUN;
proc print data=calatori;
run;

data set1;
set pret_nou(KEEP=Traveler_name Pret_Nou);
run;

data set2;
set durata(KEEP=Traveler_name  durata_zile);
RUN;

DATA combinare;
Merge set1 set2;
do
Total_nou=durata_zile*Pret_Nou;
end;
RUN;

PROC PRINT DATA=combinare;
RUN;
data set3;
set pret_nou(KEEP=Destination Accommodation_type Accommodation_cost);
run;

data set4;
set travel(KEEP=Destination Traveler_name );
RUN;

proc sql;
  create table set_combinat as
  select * from set3 as a full join set4 as b
  on A.Destination = B.Destination;
quit;
PROC PRINT DATA=set_combinat;
RUN;



data setnou;
infile datalines dlm='/';
INPUT Traveler_name $0-14 Pret_Nou ;
DATALINES;
Bogdan Andreea 4111
Elena Andrei   2444
Soare Alina    455
;
run;

DATA concatenare;
SET set1 setnou;
RUN;
PROC PRINT DATA=CONCATENARE;
RUN;

PROC MEANS DATA = travel;    
   VAR Accommodation_cost;
   output out=cost_mediu n=Num_observatii mean=Cost_mediu;
   TITLE 'Raportul vanzarilor lunare de bulbi de flori';
RUN;

proc sgplot data=cost_mediu;
  vbar Accommodation_type / response=Cost_mediu;
  xaxis display=(nolabel);
  yaxis label="Cost mediu";
run;




