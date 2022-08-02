create database dress_sales;
use dress_sales;

create table if not exists dress_master(
`Dress_ID` varchar(30),	
`Style`	varchar(30),	
`Price`	varchar(30),	
`Rating`	varchar(30),	
`Size`	varchar(30),	
`Season`	varchar(30),	
`NeckLine`	varchar(30),	
`SleeveLength` varchar(30),		
`waiseline`	varchar(30),	
`Material`	varchar(30),	
`FabricType`	varchar(30),	
`Decoration`	varchar(30),	
`PatternType` varchar(30),		
`Recommendation` varchar(30))
;

create table if not exists dress_sales(
Sale_date date,
Dress_ID varchar(30),
Quantity int
)
;