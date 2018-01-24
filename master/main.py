import googlemaps
from datetime import datetime, timedelta, date
import datetime as dt
import json, sys
import os
import time

class GoogleMaps():
    def __init__(self):
        self.gmaps = googlemaps.Client(key='AIzaSyDYDJDxaIYU4qldIMUS1mSM6pdCWpcdj2g')


    def get_minimum_distance(self, origins, destinations):
        matrix = self.gmaps.distance_matrix(origins, destinations)
        return matrix


class Routes():

    def __init__(self,  user_input_time, input_first_stop, input_final_stop, n_busses):
        self.user_input_time = user_input_time
        self.input_first_stop = input_first_stop
        self.input_final_stop = input_final_stop
        self.n_busses = n_busses
        try:
            script_dir = os.path.dirname(__file__)
            print("script ="+script_dir)
            path = os.path.join(script_dir, "routes_dtc_cfati_new.json")
            # path = '/master/routes_dtc_cfati_new.json'
            print('path ='+path)
            data = json.load(open(path))
            # print('data ='+str(data))
            data_U = data[0] # FORWARD ROUTE
            data_D = data[1]  # FORWARD ROUTE
            self.data = self.get_route_type(data_U, data_D)
        except FileNotFoundError:
            print('Please insert "routes_dtc_cfati.json" in the same folder where python script is ')
            print('Exiting program ...')
            sys.exit(0)
        except AttributeError:
            print('The data is not in the desired format.')
            print('Exiting program ...')
            sys.exit(0)

    def get_route_type(self, data_U, data_D):
        for i in range(len(data_U['stop_details'])):
            if (self.input_first_stop == data_U['stop_details'][i]['stop_name']):
                seq_start = int(data_U['stop_details'][i]['stop_seq'])
            if (self.input_final_stop == data_U['stop_details'][i]['stop_name']):
                seq_final = int(data_U['stop_details'][i]['stop_seq'])

        route = None
        if seq_start < seq_final:
            A = (data_U['first_stop_lat'], data_U['first_stop_long'])
            B = (data_U['last_stop_lat'], data_U['last_stop_long'])
            route = data_U
        else:
            A = (data_D['first_stop_lat'], data_D['first_stop_long'])
            B = (data_D['last_stop_lat'], data_D['last_stop_long'])
            route = data_D

        print('route ='+str(route))
        return route

    def validate_variables(self):
        try:
            dt_obj = datetime.strptime(self.user_input_time, '%d.%m.%Y %H:%M:%S')
            print("dt_obj ="+str(dt_obj))
            user_input_time = float(time.mktime(dt_obj.timetuple()))
        # user_input_time = float(dt_obj.timestamp())
        except AttributeError:
            print('Datetime variable is not in the desired for format.'
                  'The desired format is "%d.%m.%Y %H:%M:%S"')
            print('Exiting program ...')
            sys.exit(0)

        try:
            input_first_stop = str(self.input_first_stop).lower()
            input_final_stop = str(self.input_final_stop).lower()
        except AttributeError:
            print('Stop names must be string values and must match the exact stop name')
            print('Exiting program ...')
            sys.exit(0)
        try:
            n_busses = int(self.n_busses)
            if n_busses < 1:
                raise ValueError('Number of busses must be at least one to determine a route')
        except TypeError:
            print('Number of busses must be an integer value')
            print('Exiting program ...')
            sys.exit(0)
        return [user_input_time, input_first_stop, input_final_stop, n_busses]


    def get_route_information(self, validated_variables):
        user_input_time, input_stop, input_final_stop, number_of_buses = validated_variables
        all_stops = self.data['stop_details']
        running_times = [x['start_time'] for x in self.data['running_frequency']]

        # ROUTE START AND END COORDINATES
        A = (self.data['first_stop_lat'], self.data['first_stop_long'])
        B = (self.data['last_stop_lat'], self.data['last_stop_long'])

        for nearest_stop in all_stops:
            if (nearest_stop['stop_name'] == input_stop):
                Y = (nearest_stop['stop_lat'], nearest_stop['stop_long'])

            if (nearest_stop['stop_name'] == input_final_stop):
                Z = (nearest_stop['stop_lat'], nearest_stop['stop_long'])

        obj = GoogleMaps()
        get_distance_from_A_Y = obj.get_minimum_distance(A, Y)
        distace_A_Y = float(str(get_distance_from_A_Y['rows'][0]['elements'][0]['distance']['text']).split(' ')[0])
        duration_A_Y = int(str(get_distance_from_A_Y['rows'][0]['elements'][0]['duration']['text']).split(' ')[0])

        print('Distance from nearest stop to First stop: {} meter/km(s)'.format(distace_A_Y))
        print('Time takes to reach from First stop to nearest user stop: {} min(s)'.format(duration_A_Y))

        bus_must_leave_after = user_input_time - timedelta(minutes=duration_A_Y).total_seconds()  # IN UNIX
        bus_must_leave_after = datetime.fromtimestamp(bus_must_leave_after)  # IN NORMAL TIME
        bus_must_leave_after = datetime.strftime(bus_must_leave_after, '%H:%M:%S %p')
        bus_must_leave_after = datetime.strptime(bus_must_leave_after, '%H:%M:%S %p').time()  # PARSE ONLY TIME
        print('According to user input time, the bus had to leave after: {}'.format(bus_must_leave_after))

        bus_scheduled_time = []
        multiple_buses = 0
        for time in running_times:
            time = datetime.strptime(time, '%H:%M:%S %p').time()
            if (bus_must_leave_after < time):
                bus_scheduled_time.append(time)
                print('Scheduled buses left at: {}'.format(time))
                multiple_buses += 1
                if (multiple_buses == number_of_buses): break

        all_schedules = []
        for schedule in bus_scheduled_time:
            print('Schedule for bus leaving at {}'.format(schedule))
            time_bus_will_reach = (datetime.combine(dt.date(1, 1, 1), schedule) + timedelta(minutes=duration_A_Y)).time()
            user_input_time_time = datetime.fromtimestamp(user_input_time).time()
            ETA = datetime.combine(date.today(), time_bus_will_reach) - datetime.combine(date.today(),
                                                                                         user_input_time_time)
            print('Estimated time of arrival at the user nearest bus stop: {}'.format(ETA))

            get_distance_from_Y_Z = obj.get_minimum_distance(Y, Z)
            distace_Y_Z = float(str(get_distance_from_Y_Z['rows'][0]['elements'][0]['distance']['text']).split(' ')[0])
            duration_Y_Z = int(str(get_distance_from_Y_Z['rows'][0]['elements'][0]['duration']['text']).split(' ')[0])

            bus_reach_final_destination = (
            datetime.combine(date(1, 1, 1), time_bus_will_reach) + timedelta(minutes=duration_Y_Z)).time()
            print("Time at which you'll reach your destination is {}".format(bus_reach_final_destination))
            print('Total Distance user travel: {}'.format(str(get_distance_from_Y_Z['rows'][0]['elements'][0]['distance']['text'])))
            print('***********************')
            data = {'bus_eta': format(ETA), 'time_to_destination': format(bus_reach_final_destination),
                    'total_distance': distace_Y_Z, 'user_get_in': Y, 'user_get_out': Z}
            all_schedules.append(data)

        # with open('data.json', 'w') as fp:
        #     json.dump(all_schedules, fp)
        return all_schedules



# USAGE
# from MainUpdated import Routes
# input_time = '07.01.2018 09:04:42' # MUST BE STRING AND FOLLOWS THIS FORMAT
# input_stop = str('Turkman Gate').lower() # MUST BE STRING BUT CAN BE CASE INSENTIVE BECAUSE I AM USING LOWERCASE
# input_final_stop = str('Ganesh Nagar').lower() # MUST BE STRING BUT CAN BE CASE INSENTIVE BECAUSE I AM USING LOWERCASE
# number_of_buses = 1 # MUST BE INTEGER
# 
# obj = Routes(input_time, input_stop, input_final_stop, number_of_buses)
# variables = obj.validate_variables()
# result_data = obj.get_route_information(variables)
