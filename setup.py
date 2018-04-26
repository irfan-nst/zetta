from setuptools import setup

setup(name='zetta',
      packages=['zetta'],  # this must be the same as the name above
      version='0.1.1',
      description='Simple python framework',
      author='Irfan Nasution',
      author_email='mhmmad.irfan@gmail.com',
      url='https://github.com/irfan-nst/zetta',  # use the URL to the github repo
      keywords=['kira', 'python', 'framework'],  # arbitrary keywords
      classifiers=[],
      license='MIT',
      install_requires=[
          'flask',
          'influxdb'
      ])

