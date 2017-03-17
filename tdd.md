- looping through the directories
  - [x] it should default to `E:\CPV` for the processing
  - [x] it should accept a folder as an argument
  - [x] it should not include the directories `Assemblies`, `CPV_Base_Files`, and `CPVImpExp` in it's processing
    - [x] it should include all other folders
- parsing folder name
  - [x] it should extract the Project Name from the folder name
    - eg) `ProjectName = LAMETRO` given a folder named `LAMETRO_impexp_lametro_CPV_ARCADIA`
  - [x] it should extract he Node Name from the folder name
    - eg) `NodeName = ARCADIA` given a folder named `LAMETRO_impexp_lametro_CPV_ARCADIA`
- writing to file within each project/node folder
  - it should open the configuration xml file
    - eg) `FileName = CPV_lametro_batchCPVimpexp.xml` given `ProjectName = LAMETRO`
  - it should insert the new xml fields directly after the `<add key="OtherFiles" ...>` field
  - it should write the following, given `ProjectName = LAMETRO`
    ```xml
    <add key="UseFixedLogName" value="True" />
    <add key="FixedLogName" value="E:\CPV\TWLAMETRO_impexp_lametro_CPV_ACTON\EX-CPV_ACTON.log" />
    ```
