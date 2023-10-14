Lỗi can't compare datetime and int. 

Lỗi này gặp khi sau khi hoàn thành timed exam, vào lại trang làm bài thì không được. 

Nơi phát sinh: /openedx/edx-platform/./lms/djangoapps/course_api/blocks/transformers/block_completion.py

Fix: có ai đó đã fix nhưng code fix đã bị comment out => uncomment. 

