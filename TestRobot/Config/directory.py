# coding = utf-8
import os

curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

yaml_dir = os.path.join(curr_dir, "Yaml")
yaml_names = list(filter(None, [y if '.yaml' in y else None for y in os.listdir(yaml_dir)]))
case_dir = os.path.join(curr_dir, 'TestCase', 'Case')
bus_dir = os.path.join(curr_dir, 'TestCase', 'Business')
media_dir = os.path.join(curr_dir, 'TestRobot', 'media')
