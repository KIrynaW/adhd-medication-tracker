# Testing Page
## Table of Contents
 [**Testing Phase**](#testing-phase)
  * [***Bugs***](#bugs)
  * [***Validator Testing***](#validator-testing)
  * [***Accessibility Testing***](#accessibility-testing)
  * [***Manual Testing***](#manual-testing)
  * [***User Story Testing***](#user-story-testing)

  ***

  ## **Testing Phase:**
  ### **Bugs**

  ### **Validator Testing**

  ![](docs/screenshots/pep8_validation_result.jpg)

  ### **Accessibility Testing:**

  ![](docs/screenshots/lighthouse_accessibility.jpg)

  ### **Manual Testing**
  Test adding new medication:

  ![](docs/screenshots/testing/new_med_test.jpg)

  ![](docs/screenshots/testing/new_med_prompt_test.jpg)

  ![](docs/screenshots/testing/new_med_prompt_no_test.jpg)

  Testing creation of new logs:<br>
  ![](docs/screenshots/testing/create_log_test.jpg)

  ![](docs/screenshots/testing/log_med_test.jpg)

  Testing creation of data for logs:
  - Enter name and dose:<br>
      ![](docs/screenshots/testing/log_med_dose_test.jpg)

  - Enter day itake:<br>
      ![](docs/screenshots/testing/day_intake_test.jpg)

  - Enter First,second, third dose:<br>
      ![](docs/screenshots/testing/dose_one_test.jpg)

  - Enter Efficacy:<br>
      ![](docs/screenshots/testing/efficacy_test.jpg)

  - Enter side effects:<br>
      ![](docs/screenshots/testing/side_effects_test.jpg)

  - Enter note:<br>
      ![](docs/screenshots/testing/note_test.jpg)

  Test viewing of log history:

  - Date validation:<br>
      ![](docs/screenshots/testing/view_log_date_test.jpg)

  - Results when existing date log is entered:<br>
      ![](docs/screenshots/testing/view_date_testing_two.jpg)

  Test viewing the statistics:

  - Wrong medication input:<br>
      ![](docs/screenshots/testing/view_stats_test.jpg)

  - Exit or Return prompt when wrong input:<br>
      ![](docs/screenshots/testing/new_med_prompt_no_test.jpg)

      ![](docs/screenshots/testing/return_exit_test.jpg)

      ![](docs/screenshots/testing/exit_return_test_two.jpg)





  ### **User Story Testing**

 |No. |Story                |Pass/Fail|Evidence                     | 
 |----|---------------------|---------|-----------------------------|
 |No.1|**As a person with ADHD**, <br> I want to be able to created new medication files to which i can log daily logs and be encouraged to stay consistent  <br><br> **I know I can do it when I can open the application and be able to add new medication and new daily logs with ease, without an option of backdating the logs.**|Pass|The user is able to do it by selecting **Option 1** from the menu and creating a new medication by inputing the name of it and imedietly being prompted to create a new log without having to go back to main menu.The current date log is automatically generated and it is not possible to create a backdated log, which encourages the user to log every day <br>![Add new medication and a log](docs/screenshots/option_one.jpg)<br> ![Log already exists message](docs/screenshots/log_exists_skip.jpg)|
 |No.2|**As a person with ADHD**, <br> I want to see a daily log of my medication usage so that I can understand my medication patterns. <br><br> **I know I can do it when I can input the date of the log that I made and see all the details of the log in an ordered list.**|Pass|The user can access their log history by choosing **Option 3** in the main menu and inputing the date of the log they like to view. Then the user is shown all the details of their log for that day.<br> ![Option three chosen](docs/screenshots/option_three.jpg)<br> ![Show log history for chosen date](docs/screenshots/option_three_result.jpg)|
 |No.3|**As a person with ADHD**, <br> I want to be able to record my daily dose intake, missed doses,the medication effectiness, side effect presence and comment on general experience <br><br> **I know I can do it if there is an easy and clearn input direction .**|Pass|The user is able to do it by choosing an **Option 2** in the main menu, then inputing the medication they like to create the log for and filling all the relevant information to their medication intake. The data is then stored in the google sheets.<br> ![Creating a new log](docs/screenshots/option_two.jpg)|
 |No.4|**As a psychiatrist**, <br> I want to view my patients medication adherence data and track the effectiveness of different medications over time so I can optimize their treatment plan<br><br> **I know I can do it when I can access my patients medication efficacy, missed doses and side effect presence evaluations over sertain period of time.**|Pass|The user can do it by accessing the link to the application from their patient. In the main menu, the user can select **Option 4**, then input the name of medication to evaluate, which then generates a result based on all the present logs and stores them in a google sheet worksheet called "Results"<br> ![Option four choice input medication name](docs/screenshots/option_four.jpg)<br>![Result based on medication chosen](docs/screenshots/evaluate_meds.jpg)
|
