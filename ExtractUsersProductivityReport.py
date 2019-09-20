import sys
import configparser
import pyodbc
import datetime
import prettytable

def main():
    try:
        tool_configuration = configparser.ConfigParser()

        ini_path = sys.path[0] + '\configurationFile.ini'
        tool_configuration.read(ini_path)

        default_settings = tool_configuration["DEFAULT"]

        server_name = default_settings["server_name"]
        database_name1 = default_settings["database_name1"]
        database_name2 = default_settings["database_name2"]
        database_user_id = default_settings["user_id"]
        database_password = default_settings["database_password"]

        input_date_from = input("Please enter date from value to begin with(E.g. YYYY-MM-DD):")
        input_date_to = input("Please enter date to value to end with(E.g. YYYY-MM-DD):")

        if datetime.datetime.strptime(input_date_from, '%Y-%m-%d') is not None and \
                datetime.datetime.strptime(input_date_to, '%Y-%m-%d') is not None:
            input_facility_code = input("Please enter facility code(1 -> Mandaue or 2 -> Legaspi)")

            if len(input_facility_code) == 0:
                print("Empty facility code found!")
            else:
                sql_statement = "select tblNC.[Publication Number], " \
                                    "JobName, " \
                                    "ExternalReference, " \
                                    "UserName, " \
                                    "max([NoCorrectionRef]) as \"No Correction Made\", " \
                                    "TotalCheck, " \
                                    "TotalDedup, " \
                                    "TotalReference, " \
                                    "max(DateProcessed) as \"Date Processed\"" \
                                "from [tblNoCorrection] as \"tblNC\"" \
                                "inner join [wms_Jobs] as \"jobs\" " \
                                    "on tblNC.[Publication Number] = REPLACE(jobs.ExternalReference,'.pdf','')" \
                                "inner join [tblRefTaggerProductivity] as \"Prod\" " \
                                    "on jobs.JobName = Prod.BatchName" \
                                "where [Publication Number] is NULL " \
                                    "and DateProcessed between '2019-09-10' and '2019-09-12'" \
                                "group by [Publication Number], " \
                                    "JobName, " \
                                    "ExternalReference, " \
                                    "UserName, " \
                                    "TotalReference, " \
                                    "TotalCheck, " \
                                    "TotalDedup" \
                                "order by [Date Processed] asc"
                use_database = database_name1 if input_facility_code == '1' else database_name2
                #breakpoint()
                conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=' + server_name + ';'
                                      'Database=' + use_database + ';'
                                      'UID=' + database_user_id + ';'
                                      'PWD=' + database_password + ';'
                                      'Trusted_Connection=No')

                cursor = conn.cursor()
                cursor.execute(sql_statement)

                for row in cursor:
                    print(row)

    except Exception as e:
        print(f"Error occurred: {e}")


main()
