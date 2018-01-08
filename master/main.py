import googlemaps
from datetime import datetime, timedelta, date
import datetime as dt
import json

class GoogleMaps():
    def __init__(self):
        self.gmaps = googlemaps.Client(key='AIzaSyDYDJDxaIYU4qldIMUS1mSM6pdCWpcdj2g')


    def get_minimum_distance(self, origins, destinations):
        matrix = self.gmaps.distance_matrix(origins, destinations)
        return matrix


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-datetime', required=True)
    parser.add_argument('-neareststop', required=True)
    parser.add_argument('-finalstop', required=True)
    parser.add_argument('-n_busses', required=True)
    args = parser.parse_args()
    try:
        dt_obj = datetime.strptime(args.datetime, '%d.%m.%Y %H:%M:%S')
        user_input_time = int(dt_obj.timestamp())
        input_stop = str(args.neareststop)
        # user_input_time = int(datetime.timestamp(datetime.now()))
        input_final_stop = str(args.finalstop)
        number_of_buses = int(args.n_busses)
    except AttributeError:
        print('Please input the variables in a correct format')
        import sys
        sys.exit(0)

    # dt_obj = datetime.strptime('07.01.2018 06:38:42', '%d.%m.%Y %H:%M:%S')
    # user_input_time = float(dt_obj.timestamp())
    # input_stop = str('Trilok Puri Blk-26(Gurudwara)')
    # # user_input_time = int(datetime.timestamp(datetime.now()))
    # input_final_stop = str('Pandav Nagar Police Station')
    # number_of_buses = 5

    try:
        path = 'routes_dtc_cfati.json'
        data = json.load(open(path))
        data = data[0]  # take only one route
    except FileNotFoundError:
        print('Please insert "routes_dtc_cfati.json" in the same folder where python script is ')
    except AttributeError:
        print('The data is not in the desired format.')


    all_stops = data['stop_details']
    running_times = [x['start_time'] for x in data['running_frequency']]

    # ROUTE START AND END COORDINATES
    A = (data['first_stop_lat'], data['first_stop_long'])
    B = (data['last_stop_lat'], data['last_stop_long'])

    for nearest_stop in all_stops:
        if (nearest_stop['stop_name'] == input_stop):
            Y = (nearest_stop['stop_lat'] ,nearest_stop['stop_long'])

        if (nearest_stop['stop_name'] == input_final_stop):
            Z = (nearest_stop['stop_lat'], nearest_stop['stop_long'])

    obj = GoogleMaps()
    get_distance_from_A_Y = obj.get_minimum_distance(A, Y)
    distace_A_Y = float(str(get_distance_from_A_Y['rows'][0]['elements'][0]['distance']['text']).split(' ')[0])
    duration_A_Y = int(str(get_distance_from_A_Y['rows'][0]['elements'][0]['duration']['text']).split(' ')[0])

    print('Distance from nearest stop to First stop: {} meter/km(s)'.format(distace_A_Y))
    print('Time takes to reach from First stop to nearest user stop: {} min(s)'.format(duration_A_Y))

    bus_must_leave_after = user_input_time - timedelta(minutes=duration_A_Y).total_seconds() # IN UNIX
    bus_must_leave_after = datetime.fromtimestamp(bus_must_leave_after) # IN NORMAL TIME
    bus_must_leave_after = datetime.strftime(bus_must_leave_after, '%H:%M:%S %p')
    bus_must_leave_after = datetime.strptime(bus_must_leave_after, '%H:%M:%S %p').time() # PARSE ONLY TIME
    print('According to user input time, the bus had to leave after: {}'.format(bus_must_leave_after))

    bus_scheduled_time = []
    multiple_buses = 0
    for time in running_times:
        time = datetime.strptime(time, '%H:%M:%S %p').time()
        if (bus_must_leave_after<time):
            bus_scheduled_time.append(time)
            print('Scheduled buses left at: {}'.format(time))
            multiple_buses += 1
            if (multiple_buses == number_of_buses): break

    all_schedules = []
    for schedule in bus_scheduled_time:
        print('Schedule for bus leaving at {}'.format(schedule))
        time_bus_will_reach = (datetime.combine(dt.date(1,1,1),schedule) + timedelta(minutes=duration_A_Y)).time()
        user_input_time_time = datetime.fromtimestamp(user_input_time).time()
        ETA = datetime.combine(date.today(), time_bus_will_reach) - datetime.combine(date.today(), user_input_time_time)
        print('Estimated time of arrival at the user nearest bus stop: {}'.format(ETA))

        get_distance_from_Y_Z = obj.get_minimum_distance(A, Z)
        distace_Y_Z = float(str(get_distance_from_Y_Z['rows'][0]['elements'][0]['distance']['text']).split(' ')[0])
        duration_Y_Z = int(str(get_distance_from_Y_Z['rows'][0]['elements'][0]['duration']['text']).split(' ')[0])

        bus_reach_final_destination = (datetime.combine(date(1,1,1),time_bus_will_reach) + timedelta(minutes=duration_Y_Z)).time()
        print("Time at which you'll reach your destination is {}".format(bus_reach_final_destination))
        print('Total Distance user travel: {}'.format(distace_Y_Z))
        data = {'bus_eta': format(ETA), 'time_to_destination': format(bus_reach_final_destination),
                'total_distance': distace_Y_Z, 'user_get_in': Y, 'user_get_out': Z}
        all_schedules.append(data)

    with open('data.json', 'w') as fp:
        json.dump(all_schedules, fp)
