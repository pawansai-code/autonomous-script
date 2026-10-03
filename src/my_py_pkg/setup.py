from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pawan',
    maintainer_email='pawan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher_node = my_py_pkg.publisher:main',
            'subscriber_node = my_py_pkg.subscriber:main',
            'add_two_server = my_py_pkg.add_two_server:main',
            'my_arm_test = my_py_pkg.arm_disarm:main',
            'my_flight_test = my_py_pkg.takeoff_land:main',
        ],
    },
)
