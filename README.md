# Automated_attendance_system_using_face_recognition
This project enables you to take attendance of your class just by opening your camera for few seconds

In 'final_db_saver' change path to whatever path you have to your attendees photos with their respective names, from which we will derive encoding to later compare faces, 
for which you have to run the file 'final_run', it will open up your camera and keep identifying the faces and recording them to the 'Attendance.csv'

We have used HOG approach for face detection and the "68 face landmarks" for warping the faces and to generate encodings using a CNN model. Then we compare the captured face by 
1) Comparing its encodings with the saved encodings database.
2) By feeding it to the Classifier model which we have created using initial facial data we have taken to register the attendees.


In terminal, run - python setup.py build to generate it's executeable file
