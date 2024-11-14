import datetime
import unittest
from unittest.mock import patch

import event_planner

class TestEventPlanner(unittest.TestCase):

    def setUp(self):
        """ we use input for force or not insert conflict,
            we mock input for say not insert conflict, in test case when we
            would insert conflict we set input to 'o' """
        event_planner.input = lambda x : 'n'
        self.planner = event_planner.EventPlanner()

    def tearDown(self):
        event_planner.input = input
        self.planner = None

    # test add_event start section
    def test_add_event_first_event_normal_time_type_string(self):
        self.assertEqual(len(self.planner.events), 0)
        self.planner.add_event('test', '0:00', '1:00')
        self.assertEqual(len(self.planner.events), 1)
        event = self.planner.events[0]
        self.assertEqual(event.name, 'test')
        self.assertIsInstance(event.start_time, datetime.time)
        self.assertEqual(event.start_time, datetime.time(
            hour=0, minute=0, second=0))
        self.assertIsInstance(event.end_time, datetime.time)
        self.assertEqual(event.end_time, datetime.time(
            hour=1, minute=0, second=0))

    def test_add_event_first_event_normal_time_type_time(self):
        self.assertEqual(len(self.planner.events), 0)
        self.planner.add_event(
            'test', datetime.time(hour=0, minute=0, second=0),
            datetime.time(hour=1, minute=0, second=0))
        self.assertEqual(len(self.planner.events), 1)
        event = self.planner.events[0]
        self.assertEqual(event.name, 'test')
        self.assertIsInstance(event.start_time, datetime.time)
        self.assertEqual(event.start_time, datetime.time(
            hour=0, minute=0, second=0))
        self.assertIsInstance(event.end_time, datetime.time)
        self.assertEqual(event.end_time, datetime.time(
            hour=1, minute=0, second=0))

    def test_add_event_two_event_without_conflict(self):
        self.assertEqual(len(self.planner.events), 0)
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.assertEqual(len(self.planner.events), 1)
        self.planner.add_event(
            'test 2', '3:00', '3:30')
        self.assertEqual(len(self.planner.events), 2)

    def test_add_event_two_event_without_conflict_just_before(self):
        self.assertEqual(len(self.planner.events), 0)
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.assertEqual(len(self.planner.events), 1)
        self.planner.add_event(
            'test 2', '0:30', '1:00')
        self.assertEqual(len(self.planner.events), 2)

    def test_add_event_two_event_without_conflict_just_after(self):
        self.assertEqual(len(self.planner.events), 0)
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.assertEqual(len(self.planner.events), 1)
        self.planner.add_event(
            'test 2', '2:00', '3:30')
        self.assertEqual(len(self.planner.events), 2)

    def test_add_event_same_name(self):
        self.planner.add_event('test', '0:00', '1:00')
        self.assertRaises(
            ValueError, self.planner.add_event, 'test', '3:00', '5:00')

    def test_add_event_start_time_wrong_type(self):
        self.assertRaises(ValueError, self.planner.add_event, 'test', 2, '5:00')

    def test_add_event_start_time_not_time_string(self):
        self.assertRaises(
            ValueError, self.planner.add_event, 'test', 'heure', '5:00')

    def test_add_event_time_out_of_range(self):
        self.assertRaises(
            ValueError, self.planner.add_event, 'test', '25:00', '26:00')

    def test_add_event_start_time_upper_than_end_time(self):
        self.assertRaises(
            ValueError, self.planner.add_event, 'test', '6:00', '5:00')

    @patch('builtins.print')
    def test_add_two_event_with_conflict_second_event_all_in_first(
            self, mock_print):
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event('test 2', '1:10', '1:30')
        self.assertEqual(len(self.planner.events), 1)
        mock_print.assert_called_with('conflits avec les événements: test')

    @patch('builtins.print')
    def test_add_two_event_with_conflict_second_event_before_first(
            self, mock_print):
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event('test 2', '0:30', '1:30')
        self.assertEqual(len(self.planner.events), 1)
        mock_print.assert_called_with('conflits avec les événements: test')

    @patch('builtins.print')
    def test_add_two_event_with_conflict_second_event_after_first(
            self, mock_print):
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event('test 2', '1:30', '2:30')
        self.assertEqual(len(self.planner.events), 1)
        mock_print.assert_called_with('conflits avec les événements: test')

    @patch('builtins.print')
    def test_add_two_event_with_conflict_force_insert(self, mock_print):
        event_planner.input = lambda x : 'o'
        self.assertEqual(len(self.planner.events), 0)
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.assertEqual(len(self.planner.events), 1)
        self.planner.add_event(
            'test 2', '1:30', '3:30')
        mock_print.assert_called_with('conflits avec les événements: test')
        self.assertEqual(len(self.planner.events), 2)

    def test_list_events_without_event(self):
        sorted_events = self.planner.list_events()
        self.assertEqual(len(sorted_events), 0)

    def test_list_events_already_in_order(self):
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event(
            'test 2', '5:00', '8:00')
        self.planner.add_event(
            'test 3', '12:00', '12:30')
        sorted_events = self.planner.list_events()
        self.assertEqual(len(sorted_events), 3)
        self.assertEqual(sorted_events[0].name, 'test')
        self.assertEqual(sorted_events[1].name, 'test 2')
        self.assertEqual(sorted_events[2].name, 'test 3')

    def test_list_events_not_in_order(self):
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event(
            'test 2', '18:00', '19:00')
        self.planner.add_event(
            'test 3', '12:00', '12:30')
        sorted_events = self.planner.list_events()
        self.assertEqual(len(sorted_events), 3)
        self.assertEqual(sorted_events[0].name, 'test')
        self.assertEqual(sorted_events[1].name, 'test 3')
        self.assertEqual(sorted_events[2].name, 'test 2')

    def test_check_conflict_without_conflict(self):
        event_planner.input = lambda x: 'o'
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event(
            'test 2', '18:00', '19:00')
        self.planner.add_event(
            'test 3', '12:00', '12:30')
        conflicts = self.planner.find_conflicts()
        self.assertEqual(len(conflicts), 0)

    def test_check_conflict_with_one_conflict(self):
        event_planner.input = lambda x: 'o'
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event(
            'test 2', '11:00', '14:00')
        self.planner.add_event(
            'test 3', '12:00', '12:30')
        conflicts = self.planner.find_conflicts()
        self.assertEqual(len(conflicts), 1)
        self.assertIsInstance(conflicts[0], tuple)
        self.assertEqual(conflicts[0][0].name, 'test 2')
        self.assertEqual(conflicts[0][1].name, 'test 3')

    def test_check_conflict_with_two_conflicts_on_same_event(self):
        event_planner.input = lambda x: 'o'
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event(
            'test 2', '1:00', '1:30')
        self.planner.add_event(
            'test 3', '1:30', '2:30')
        conflicts = self.planner.find_conflicts()
        self.assertEqual(len(conflicts), 2)
        self.assertEqual(conflicts[0][0].name, 'test')
        self.assertEqual(conflicts[0][1].name, 'test 2')
        self.assertEqual(conflicts[1][0].name, 'test')
        self.assertEqual(conflicts[1][1].name, 'test 3')

    def test_check_conflict_with_two_conflicts_on_different_event(self):
        event_planner.input = lambda x: 'o'
        self.planner.add_event(
            'test', '1:00', '2:00')
        self.planner.add_event(
            'test 2', '1:00', '1:30')
        self.planner.add_event(
            'test 3', '4:30', '5:30')
        self.planner.add_event(
            'test 4', '5:00', '6:30')
        conflicts = self.planner.find_conflicts()
        self.assertEqual(len(conflicts), 2)
        self.assertEqual(conflicts[0][0].name, 'test')
        self.assertEqual(conflicts[0][1].name, 'test 2')
        self.assertEqual(conflicts[1][0].name, 'test 3')
        self.assertEqual(conflicts[1][1].name, 'test 4')

if __name__ == '__main__':
    unittest.main()