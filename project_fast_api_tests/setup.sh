cd ../project_fast_api
docker image build . -t fraud_detection_docker:latest

cd ../project_fast_api_tests/status_tests
docker image build . -t status_tests_docker:latest

cd ../../project_fast_api_tests/welcome_message_tests
docker image build . -t welcome_message_tests_docker:latest

cd ../../project_fast_api_tests/test_performance_tests
docker image build . -t test_performance_tests_docker:latest

cd ../../project_fast_api_tests/prediction_tests
docker image build . -t prediction_tests_docker:latest

cd ..
docker-compose up --exit-code-from prediction_tests && docker-compose down
