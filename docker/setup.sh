cd ./docker/fastapi_test_status
docker image build . -t image_test_status:latest

cd ./docker/fastapi_test_welcome_message
docker image build . -t image_test_welcome_message:latest

cd ./docker/fastapi_test_performance
docker image build . -t image_test_performance:latest

cd ./docker/fastapi_test_predict
docker image build . -t image_test_predict:latest

cd ./docker/fastapi_test_random_predict
docker image build . -t image_test_random_predict:latest

cd ./docker
docker-compose up
