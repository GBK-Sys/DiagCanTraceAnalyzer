1. Provide CAN trace in asc format 
2. Include filtered log which contains only the diagnostic frame Request and Response frame for project relevent node with the desired channel
3. Do not include DBC in canoe/canalyzer configuration
4. Fill below values in config.properties file

[FILES]
input_file=Input file full path in .asc format with parsed diagnostic request & response
output_file=output file full path with file name where the output report can be generated

[CAN_IDS]
request_id = Diagnostic Request ID
response_id = Diagnostic Response ID
# Change to CAN for CAND project
[PROJECT]
type = CAN

[DDL]
DiagnosisDataListPath= DDL full path which can be either .csv or .xlxs from application container delivered to customer or if not needed keep it empty

[SETTINGS]
enable_failure_identification = True  # Set to False to skip DDL processing