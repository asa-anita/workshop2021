import pandas as pd
import numpy as np


def generate_session(df, sequence, start_hours, start_mins, end_hours, end_mins, talk_duration,
                     td_left, td_right, second_line_left, third_line_left,
                     fourth_line_left, offset=0):

    num_talks = len(df)

    # Now start iterating and generating a schedule.

    current_hour = start_hours
    current_mins = start_mins

    for talk_num in range(offset, num_talks):
        if current_mins + talk_duration >= 60:
            talk_hour_end = current_hour + 1
        else:
            talk_hour_end = current_hour
        talk_minute_end = (current_mins + talk_duration) % 60


        time_line = "{0}:{1:02d} - {2}:{3:02d}".format(current_hour, current_mins,
                                                       talk_hour_end, talk_minute_end)

        name = "{0} {1}".format(df["Name"].iloc[sequence[talk_num]],
                                df["Surname"].iloc[sequence[talk_num]])

        talk_title = df["PresentationTitle"].iloc[sequence[talk_num]]

        print("<tr>")
        print("{0}{1}{2}".format(second_line_left, time_line, td_right))
        print("{0}{1}{2}".format(third_line_left, name, td_right))
        print("{0}{1}{2}".format(fourth_line_left, talk_title, td_right))
        print("</tr>")

        # Now update the timer.
        current_mins = (current_mins + talk_duration) % 60 

        # If we clicked over to the next hour, current_mins will be less than
        # the talk duration. In this case, increment to next hour.
        if current_mins < talk_duration:
            current_hour += 1

        #print("Current Hour: {0}\tCurrent Mins {1}".format(current_hour, current_mins))
        #print("End_hours: {0}\tEnd_mins {1}".format(end_hours, end_mins))
        # Finally, check if we have now moved past the final time of the session.
        if current_hour >= end_hours and current_mins >= end_mins:
            return talk_num + 1


if __name__ == "__main__":


    session_start_hour = [9, 11, 13, 15, 9, 11, 13]
    session_end_hour = [10, 12, 15, 17, 10, 12, 15]

    session_start_min = [0, 0, 30, 30, 0, 0, 30, 30]
    session_end_min = [30, 30, 0, 0, 30, 30, 0, 0]

    talk_duration = 15
   
    second_line_left = '<td width=10% style="font-style:italic">'
    third_line_left = '<td width=15%>'
    fourth_line_left = '<td width=55%>'

    td_left = '<td>' 
    td_right = '</td>'

    fname = "./responses.csv"

    df = pd.read_csv(fname, sep=",")

    # We only want responses that are doing talks.
    df = df.dropna(subset=["PresentationTitle"])
    num_talks = len(df)
    print("There are {0} Talks to be scheduled".format(num_talks))
    exit()
    offset = 0

    sequence = np.arange(0, num_talks)
    np.random.shuffle(sequence)

    # Now we know the Session times so let's generate from there.
    for session_num in range(len(session_start_hour)):
    #for session_num in range(2):

        hour_start = session_start_hour[session_num]
        hour_end = session_end_hour[session_num]

        min_start = session_start_min[session_num]
        min_end = session_end_min[session_num]

        offset = generate_session(df, sequence, hour_start, min_start, hour_end, min_end, talk_duration,
                                  td_left, td_right, second_line_left, third_line_left,
                                  fourth_line_left, offset)

        print("")
        print("")

    ''' 
    <tr>
    <td width=10% style="font-style:italic">9:05 - 9:20 </td>
    <td width=15%>Hayley Macpherson</td>
    <td width=55%>Cosmological structure formation with numerical relativity</td>
    </tr>
    '''
