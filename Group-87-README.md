<div style="font-family: 'Times New Roman', Times, serif;">
<h1 style="text-align: center;">
    Software Engineering Processes <br>
    Group 87 <br>
    Assignment 1 - Report
</h1>

## Project chosen: 
OPSDROID - https://github.com/opsdroid/opsdroid
## **Group Members:**
Aryan Kheskani Raisinghani (akh203), Gaelle Nehme (gne201), Aryan Rajput (ara289), Gonzalo Lantero (gla201)

## **Repository URL:** https://github.com/AryanKheskani/SEP-87-opsdroid

### Number of lines of code and the tool used to count it: 
Kloc = 25.6, Tool used = Lizard
![Screenshot 2024-06-24 at 17.04.50](https://hackmd.io/_uploads/S1hXiWwU0.png)

### **Programming language:** 
Python

### **Coverage measurement:**
Existing tool - Coverage.py

### **Coverage results**
The coverage result is different for different devices: 
#### From a MacBook Air M2:
![Screenshot 2024-06-24 at 17.08.08](https://hackmd.io/_uploads/BkNl3WPIR.png)

#### From a MacBook Air M1:
![Screenshot 2024-06-24 at 17.07.17](https://hackmd.io/_uploads/Bko2iZwUA.png)

#### From a MacBook Pro M3:
![Screenshot 2024-06-24 at 17.08.15](https://hackmd.io/_uploads/HkM-2WvLC.png)


#### **Note:**
“opsdroid is currently slowly migrating from unittest to pytest as its testing framework [...] As a part of this migration tests can be found in one of two places, old unittest tests are found in the tests/ directory in the root of the repository and new pytest tests are found in a tests/ directory in the same subfolder as the code, i.e opsdroid/tests/.”

Therefore, to measure the coverage for opsdroid_logging.py, we used pytest, while to measure that of constraints.py and memory.py we used unittest.

## Your own coverage tool
Since we observed different results from different laptops or some of us were not able to run it to begin with, we decided to work together and collaborate through VSCode Live Share. Each of us worked on two separate functions, but we tested and ran our coverage tool on one laptop; therefore, we have one fork instead of four. 

The coverage tool is implemented through multiple functions that initialise, mark, and report coverage of branches within specific functions.  To ensure complete branch coverage, our coverage tool needs to account for both the "if" and "else" branches in the code. So we added “invisible”  else statements (empty else statements with a markup) so that the branch can be marked whenever a conditional statement is encountered.

**Aryan Kheskani Raisinghani** and **Gaelle Nehme** both worked on the **opsdroid_logging.py** file, Aryan did the coverage for 3 functions (as I wasn't sure initially if I was doing it correctly) and Gaelle did the other 2. Example usages were added to pass arguments into each function, with branch coverage being based on these examples serving as tests.

We all made some helper functions to help us with the instrumentation, so that code wasn’t repeated

![Screenshot 2024-06-24 at 17.08.13](https://hackmd.io/_uploads/Bk6xn-vLA.png)


### **Group Member: Aryan Kheskani Raisinghani**
#### **Function 1: funcParsingFilter.__init**
1. Coverage initialisation:
    
![Screenshot 2024-06-24 at 17.09.52](https://hackmd.io/_uploads/rkCIhZPLA.png)

2. Code with instrumentation:
    
![Screenshot 2024-06-24 at 17.10.48](https://hackmd.io/_uploads/rkKY2ZDI0.png)

3. Example Usage:
    
![Screenshot 2024-06-24 at 17.23.50](https://hackmd.io/_uploads/BJIakzP8C.png)

4. Coverage results output by the instrumentation:
    
![Screenshot 2024-06-24 at 17.15.17](https://hackmd.io/_uploads/ryxrkMDIR.png)


#### **Function 2: parsingFilter.filter**
1. Coverage initialisation: 
    
![Screenshot 2024-06-24 at 17.25.23](https://hackmd.io/_uploads/SktRezPIR.png)

2. Code with instrumentation:
    
![Screenshot 2024-06-24 at 17.29.35](https://hackmd.io/_uploads/B1ugWzD8C.png)

3. Example Usage:
    
![Screenshot 2024-06-24 at 17.30.06](https://hackmd.io/_uploads/rkzGbGDI0.png)

4. Coverage results output by the instrumentation:
    
![Screenshot 2024-06-24 at 17.31.31](https://hackmd.io/_uploads/HyOvbMvLC.png)


#### **Function 3: configure_logging**
1. Coverage initialisation: 
    
![Screenshot 2024-06-24 at 17.32.18](https://hackmd.io/_uploads/r1z9WMPI0.png)

2. Code with instrumentation:
    
![Screenshot 2024-06-24 at 17.33.06](https://hackmd.io/_uploads/r1VpZMv80.png)
![Screenshot 2024-06-24 at 17.33.31](https://hackmd.io/_uploads/rymrzzDLR.png)

3. Example Usage:
    
![Screenshot 2024-06-24 at 17.35.51](https://hackmd.io/_uploads/SJCPGfvI0.png)

4. Coverage results output by the instrumentation:
    
![Screenshot 2024-06-24 at 17.36.19](https://hackmd.io/_uploads/SJVYGzwUC.png)


### Group Member: Gaelle Nehme
#### Function 1: set_formatter_string
1. Coverage initialisation:
    
![Screenshot 2024-06-24 at 17.10.12](https://hackmd.io/_uploads/SkQo3WPLC.png)
		
2. Code with instrumentation: 
    
![Screenshot 2024-06-24 at 17.10.18](https://hackmd.io/_uploads/Sy2n2-P80.png)

3. Example Usage:
    
![Screenshot 2024-06-24 at 17.10.26](https://hackmd.io/_uploads/B1Np3bPUR.png)

4. Coverage results output by the instrumentation:
    
![Screenshot 2024-06-24 at 17.10.32](https://hackmd.io/_uploads/Byab6-v8R.png)

#### Function 2: get_logging_level
1. Coverage initialisation: 
    
![Screenshot 2024-06-24 at 17.10.43](https://hackmd.io/_uploads/ryKGTbDLR.png)

2. Code with instrumentation:
    
![Screenshot 2024-06-24 at 17.10.49](https://hackmd.io/_uploads/ryiQa-D8C.png)

3. Example Usage:
    
![Screenshot 2024-06-24 at 17.10.56](https://hackmd.io/_uploads/ryDHTWwIA.png)

4. Coverage results output by the instrumentation:
    
![Screenshot 2024-06-24 at 17.11.04](https://hackmd.io/_uploads/B1D8aWPLA.png)


### Group Member: Gonzalo Lantero
#### Function 1: _get_from_database
1. Coverage initialisation: 
![Screenshot 2024-06-24 at 17.02.52](https://hackmd.io/_uploads/rJ7pibv8A.png)

2. Code with instrumentation:
![Screenshot 2024-06-24 at 17.03.07](https://hackmd.io/_uploads/SkyRobwLA.png)

3. Coverage results output by the instrumentation:
![Screenshot 2024-06-24 at 17.03.19](https://hackmd.io/_uploads/r1HCjbPLC.png)

#### Function 2: _put_to_database
1. Coverage initialisation:
![Screenshot 2024-06-24 at 17.03.29](https://hackmd.io/_uploads/rkC0o-DLA.png)


2. Code with instrumentation:
![Screenshot 2024-06-24 at 17.03.37](https://hackmd.io/_uploads/HkVJhWwLC.png)


3. Coverage results output by the instrumentation:
![Screenshot 2024-06-24 at 17.03.46](https://hackmd.io/_uploads/HJ213ZwUR.png)


### Group Member: Aryan Rajput

#### Function 1: def run()
1. Initialisation:
![Screenshot 2024-06-24 at 9.13.43 PM](https://hackmd.io/_uploads/B1NBVzvIC.png)


2. Code with instrumentation:
![Screenshot 2024-06-24 at 9.12.58 PM](https://hackmd.io/_uploads/HJfQ4MvLR.png)

3. Example Usage:
![Screenshot 2024-06-24 at 9.12.29 PM](https://hackmd.io/_uploads/HkteEzvU0.png)


4. Coverage results output by the instrumentation:
![Screenshot 2024-06-24 at 9.11.44 PM](https://hackmd.io/_uploads/rJxCmGPIA.png)



#### Function 2: def get_parser_config()
1. Initialization
![Screenshot 2024-06-24 at 9.11.11 PM](https://hackmd.io/_uploads/rkhi7zDL0.png)


2. Code with instrumentation
![Screenshot 2024-06-24 at 9.10.28 PM](https://hackmd.io/_uploads/HknYmGwIR.png)


3. Example Usage 
![Screenshot 2024-06-24 at 9.09.49 PM](https://hackmd.io/_uploads/r198mfP8A.png)


4. Coverage results output by the instrumentation:
![Screenshot 2024-06-24 at 9.08.38 PM](https://hackmd.io/_uploads/HJw4mGPI0.png)

## **Coverage improvement**
### **Individual tests**

#### **Group Member: Aryan Kheskani Raisinghani**
#### Test 1: ParsingFilter.filter:
1. Example Usage: 
    
![Screenshot 2024-06-24 at 17.37.13](https://hackmd.io/_uploads/rkgpzGDI0.png)

2. Old coverage results: 
    
![Screenshot 2024-06-24 at 17.37.43](https://hackmd.io/_uploads/SkF0MMwLR.png)

3. New coverage results:
    
![Screenshot 2024-06-24 at 17.38.07](https://hackmd.io/_uploads/BJPlQGvLR.png)

5. Coverage improvement explanation:
    - The coverage improved by 67% and reached 100% by making sure that both the if and else branch are being tested
    - For the if branch: when self.config["filter"].get("whitelist") is True

#### Test 2: Parsing Filter.__init__:
1. Example Usage:
    
![Screenshot 2024-06-24 at 17.38.43](https://hackmd.io/_uploads/HJYfQGDU0.png)

2. Old Coverage results:
    
![Screenshot 2024-06-24 at 17.39.06](https://hackmd.io/_uploads/BJJNQGDLA.png)

3. New Coverage results:
    
![Screenshot 2024-06-24 at 17.39.27](https://hackmd.io/_uploads/Sy4H7MD8A.png)

4. Coverage improvement explanation:
    - To increase the coverage from 50% to 100%, we added to the example usage of the instrumented code since the original test did not cover all configurations of config[“filter”], as it didn't check where only either a whitelist or blacklist filter exists.  
    - We tested __init__ for all the branches, each with a different case (whitelist and blacklist filters, only whitelist filter, no whitelist or blacklist filter, only blacklist filter)  
        - Branch 0 is tested with config_case1 where both whitelist and blacklist 
        - Branch 1 is tested with config_case2 where either whitelist or blacklist filters
        - Branch 1 is also tested with config_case4 where only blacklist filter exists
        - Branch 2 is tested with config_case3 where neither a blacklist or whitelist filter to try with a keyError exception that is raided due to a missing filter key

#### Group Member: Gaelle Nehme
#### Test 1: set_formatter_string
1. Example Usage:
    
![Screenshot 2024-06-24 at 17.15.00](https://hackmd.io/_uploads/ryDp6bD8C.png)
    
    ![Screenshot 2024-06-24 at 17.15.06](https://hackmd.io/_uploads/H1s1C-wIA.png)

2. Old Coverage Results:
    
![Screenshot 2024-06-24 at 17.15.14](https://hackmd.io/_uploads/SkOwAbDLA.png)

3. New Coverage Results:
    
![Screenshot 2024-06-24 at 17.15.22](https://hackmd.io/_uploads/r1S_AWvLR.png)


4. Coverage improvement explanation 
    - The branch coverage increased from 66.7% to 100% by ensuring that all branches are reached.
        - Branch 0 is tested by config_case4 which provides a “costom_formatter” in the configuration
        - Branch 1 is tested by config_case1 and config_case5 which enables the “extended” option in the configuration 
        - Branch 2 is tested by config_case1 which enables the “timestamp” option in the configuration 

#### Test 2: get_logging_level
1. Example Usage:
    
![Screenshot 2024-06-24 at 17.15.29](https://hackmd.io/_uploads/ry_9CWD8C.png)

2. Old coverage results:
    
![Screenshot 2024-06-24 at 17.15.36](https://hackmd.io/_uploads/rJEn0ZvLR.png)


3. New coverage results:
    
![Screenshot 2024-06-24 at 17.15.44](https://hackmd.io/_uploads/H103RZw8C.png)


4. Coverage improvement explanation 
    - The branch coverage started at 20% as only branch 3 was being executed. Therefore, by adding “example usages” or tests that ensure that the other branches were also executed, the overall branch coverage for get_logging_level increases to 100%
        - Branch 0 is tested by level_case1 when the logging level is “critical”
        - Branch 1 is tested by level_case2 when the  logging level is “error”
        - Branch 2 is tested by level_case3 when the logging level is “warning”
        - Branche 3 is tested by level_case4 when the logging level is “debug”
        - Branch 4 is tested by level_case5 when the logging level is “info” 

#### Group Member: Gonzalo Lantero
#### Test 1: _get_from_database
1. Example Usage
![Screenshot 2024-06-24 at 17.04.23](https://hackmd.io/_uploads/BkWw3-PUR.png) 

2. Old coverage results
![Screenshot 2024-06-24 at 17.04.35](https://hackmd.io/_uploads/Hy3V1zwUA.png)

3. New coverage results
![Screenshot 2024-06-24 at 17.04.43](https://hackmd.io/_uploads/Bka8yMDIC.png)


4. Coverage improvement explanation
    - The branch coverage increased from 66.7% to 100% by testing the empty memory and not only when the key was present (branch 0), the rest were already covered by the existing test.
    
#### Test 2: _put_to_database
1. Example Usage
![Screenshot 2024-06-24 at 17.05.04](https://hackmd.io/_uploads/H1Ad2bPUC.png)

2. Old coverage results
![Screenshot 2024-06-24 at 17.05.12](https://hackmd.io/_uploads/BJiF2Ww8R.png)

3. New coverage results
![Screenshot 2024-06-24 at 17.05.20](https://hackmd.io/_uploads/H1aXWMw8R.png)


4. Coverage improvement explanation
    - The coverage increased from 33.33% to 100% by reaching the first and second branch, Branch 0 and 1. This was achieved by testing the whole function if there was a database already created.
#### Group Member: Aryan Rajput
#### Test 1: def run()

1. Example Usage
![Screenshot 2024-06-24 at 9.06.47 PM](https://hackmd.io/_uploads/rkEszMvUA.png)

2. Old coverage:
![Screenshot 2024-06-24 at 9.05.55 PM](https://hackmd.io/_uploads/ryHuMGPIC.png)


3. New coverage:
![Screenshot 2024-06-24 at 9.05.16 PM](https://hackmd.io/_uploads/HJe8zzvLC.png)


4. Coverage improvement explanation

- The function coverage increased from 83% and reached 100%. In the old function, only a subset of the branch was tested, and we skipped test cases with self.running = True for run(), and the branch where the timeout condition is reached and the warning is also True. In the new code, all the branches and conditions are tested which increased the function coverage by 17% and also the branch coverage by some amout.

#### Test 2: def get_parser_config()
1. Example Usage 
![Screenshot 2024-06-24 at 8.55.10 PM](https://hackmd.io/_uploads/S1N3ZGwIC.png)

2. Old coverage:
![Screenshot 2024-06-24 at 8.54.17 PM](https://hackmd.io/_uploads/rJdnkGPUC.png)

3. New coverage:
![Screenshot 2024-06-24 at 8.42.16 PM](https://hackmd.io/_uploads/H1wE1MvU0.png)

4. Coverage improvement explanation

    - The branch coverage increased by 66.6%. The existing tests here only covered the cases where modules were empty and where modules were not empty. However, the case where the module is not empty and the parser name matches a middle element in the list was skipped, which was then covered. In the new code, all the branches and conditions were tested leading to an increased overall function and branch coverage.

## **Overall opsdroid_logging.py**
### Overall input on opsdroid_logging (Aryan Kheskani & Gaelle Nehme):

Overall, for get_logging, we increased the overall branch coverage using our own coverage tool by adding multiple configurations and invoking each function with them, as the example usage ensures that all the existing branches are executed and tested. This approach resulted in significant branch coverage  improvement as it increased the overall branch coverage from 47.62 to 85.71% using our own tool. In addition, tests in the test_logging were enhanced or added to increase the coverage from 81% to 83% for opsdroid_logging using the preexisting tool. It is important to mention that although the coverage for the single file increased, the coverage of the overall coverage did not increase as it stayed at 13% after we implemented the tests. We assume that this is because of how big the project is that enhancing the coverage of a single file by 2% will not affect the overall coverage. 

### Old Coverage Results of opsdroid_logging using our own tool:
![Screenshot 2024-06-24 at 17.22.06](https://hackmd.io/_uploads/HJYIkGvUA.png)
 

### New Coverage Results of opsdroid_logging using our own tool:
![Screenshot 2024-06-24 at 17.22.17](https://hackmd.io/_uploads/HktPyGDLR.png)


### Old Coverage Results of opsdroid_logging using existing tool:
![Screenshot 2024-06-24 at 17.22.24](https://hackmd.io/_uploads/rJNdkMwIC.png)


### New Coverage Results of opsdroid_logging using existing tool:
![Screenshot 2024-06-24 at 17.22.31](https://hackmd.io/_uploads/rJ6ukMP8C.png)


## **Tests added by Aryan Kheskani**

### Test for ParsingFilter.__init__:
![Screenshot 2024-06-24 at 17.40.42](https://hackmd.io/_uploads/H1HqmGDIR.png)

### Test for Parsing.filter:
![Screenshot 2024-06-24 at 17.41.11](https://hackmd.io/_uploads/HypiQMD80.png)


## **Tests added by Gaelle Nehme**
#### Test for set_formatter_string: 
![Screenshot 2024-06-24 at 17.22.41](https://hackmd.io/_uploads/By_t1fPUA.png)


#### Test for get_logging_level: 
![Screenshot 2024-06-24 at 17.22.46](https://hackmd.io/_uploads/Bky9yGwL0.png)


## **Overall memory.py**
### Overall input (Gonzalo Lantero)
Overall, for _get_from_database and _put_to_database, I measured the change in the overall branch coverage using the Coverage.py tool. There was a significant branch coverage improvement as it shows an increase in the overall branch coverage from 19% to 54%. 
### Old Coverage Results
![Screenshot 2024-06-24 at 17.06.18](https://hackmd.io/_uploads/HkCIWMPU0.png)

### New Coverage Results
![Screenshot 2024-06-24 at 17.06.30](https://hackmd.io/_uploads/SkY9-GP8C.png)

### Tests added for _get_from_database
![Screenshot 2024-06-24 at 17.06.40](https://hackmd.io/_uploads/SJoi-zPL0.png)

### Tests added for _put_to_database
![Screenshot 2024-06-24 at 17.06.51](https://hackmd.io/_uploads/BJ53bGvLC.png)



## **Overall helper.py (Aryan Rajput)**
### Overall input (Aryan Rajput)
Overall input (Aryan Rajput)
Overall, for run() and get_parser_config(), I added and covered the test cases of ‘self.runnning’ being False and ‘self.running’ being True (for run()), and when module is not empty, the parser name matches at least one middle element in the list (for get_parser_config()). I measured the change in the overall branch coverage using the Coverage.py tool. There was a branch coverage improvement from 77% to 83%. 


### Old Coverage Results of helper.py using our own tool
![Screenshot 2024-06-24 at 8.40.22 PM](https://hackmd.io/_uploads/SJCt3-D80.png)



### New Coverage Results of helper.py using our own tool
![Screenshot 2024-06-24 at 8.38.56 PM](https://hackmd.io/_uploads/BkxQnZw8C.png)


### Old Coverage Results using existing tool
![Screenshot 2024-06-24 at 8.38.03 PM](https://hackmd.io/_uploads/Sksk3bDL0.png)

### New Coverage Results using existing tool
![Screenshot 2024-06-24 at 8.37.24 PM](https://hackmd.io/_uploads/rkFToWDLC.png)


### Added tests in the test file (test_helper.py)
![Screenshot 2024-06-24 at 8.36.31 PM](https://hackmd.io/_uploads/SJhFsWDUC.png)


## Summary



| **Names**       | **Section 3.2**                                                                                              | **Section 3.3**                                                                                     |
| --------------- |:------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Aryan Kheskani  | In the file opsdroid_logging.py:<br>- ParsingFilter__init__<br>- ParsingFilter.filter<br>- configure_logging | Increased branch coverage of ParsingFilter.__init__ and ParsingFilter.filter                        |
| Aryan Rajput    | In the file helper.py:<br>- run() <br>- get_parser_config()                                                  | Increased branch coverage of run() and get_parser_config()                                          |
| Gaelle Nehme    | In the file opsdroid_logging.py: <br> - set_formatter_string() <br> - get_logging_level                      | Increased branch coverage of ParsingFilter.set_formatter_strong and ParsingFilter.get_logging_level |
| Gonzalo Lantero | In the file memory.py: <br>- _get_from_database <br>- _put_to_database                                        | Increased branch coverage of Memory._get_from_database and Memory._put_to_database                  |

</div>