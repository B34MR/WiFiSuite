from setuptools import setup, find_packages

setup(name='WiFiSuite',
    version='v 1.05282017',
    description='Enterprise WPA Wireless Tool suite ',
    classifiers=[
        'Development Status :: 1 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Kali Linux'
    ],
    keywords='pentesting security wireless eap 802.1X radius',
    url='https://github.com/NickSanzotta/WiFiSuite',
    author='Nick Sanzotta',
    license='MIT',
    packages=find_packages(include=[
        "wifisuite", "wifisuite.*", "wifisuite.wifisuite.*"
    ]),
    install_requires=[
        'wpa_supplicant',
        'psutil',
        'netifaces'
    ],
    # entry_points = {
    #     'console_scripts': ['wifisuite=wifisuite.wifisuite:main'],
    # },
    include_package_data=True,
    zip_safe=False)
