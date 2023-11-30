## RankerHack

### Project Description
The Python script, encapsulated within a Docker container, utilizes a user-specified endpoint as a parameter for intercepting HTTPS requests. It employs a parsing mechanism to identify questions within the intercepted data and utilizes HuggingFace Language Models for response generation. The script also features functionality to recognize and exclude requests associated with various detection mechanisms.

**Key Features**

1. **HTTPS Request Interception:** RankerHack intercepts HTTPS requests directed at a user-specified web endpoint, allowing the analysis of incoming queries.

2. **Question Detection:** The script identifies questions within intercepted requests. The endpoint to be monitored is specified as a parameter, enabling flexibility in the target web domain.

3. **HuggingFace LLM Model Integration:** Leveraging HuggingFace Language Models, RankerHack formulates precise and contextually relevant responses to the detected questions.

4. **Automatic Anti-Detection Handling:** In instances where detection mechanisms, such as `left_browser` detection, are triggered within intercepted requests, RankerHack automatically handles and drops these requests, ensuring the script avoids engagement with such prompts.

5. **Image Recognition:** RankerHack can identify images within intercepted requests and generate a response based on the image's content binary data.


### How to Run the Project

**Prerequisites:**
- Docker installed on your system.

**Steps:**

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/henriqueblobato/RankerHack.git
    cd RankerHack
    ```

2. **Prepare Environment Variables:**

    - Create a `.env` file and add the necessary environment variables:
        ```plaintext
        OPENAI_API_KEY=your_openai_api_key
        HUGGING_FACE_API_KEY=your_hugging_face_api_key
        PROXY_USERNAME=
        PROXY_PASSWORD=
        ```

3. **Modify Python Script (if required):**

    - Adjust the Python script (`app.py`) to suit specific configurations or requirements, if necessary.

4. **Build the Docker Image and run it:**
    ```bash
    make
    ```
   
5. **Once its running, open your browser at the following address:**
    ```plaintext
    http://mitm.it
    ```
    - And follow the instructions to install the certificate according to your operating system.

<img width="816" alt="Screen Shot 2023-11-30 at 19 35 07" src="https://github.com/henriqueblobato/RankerHack/assets/18133417/ef441dd1-3753-430b-a02e-70da9159712f">


6. **Open your browser at assessment endpoint:**
    ```plaintext
    https://company_assessment.tst_grla.com/
    ```
    - Expect answers to be generated for the questions in the assessment.
   
### Tested on platforms:
- TestGorilla
- HackerRank
- 

#### Future Plans
- Test on more platforms and add support for additional endpoints.
- Think in a better way to show the answers to the user.
- Strengthen error handling and implement comprehensive logging for easier debugging.
- Optimize the Dockerfile to reduce image size and enhance efficiency.
- Use SOLID principles to improve code quality and maintainability.
- Explore advanced methods to maximize flexibility and scalability in utilizing Hugging Face models across various NLP applications.
- Check better ways to replace playwright or selenium.

#### Future Plan Architecture
- <img width="887" alt="Screen Shot 2023-11-30 at 19 56 48" src="https://github.com/henriqueblobato/RankerHack/assets/18133417/8565b8c1-6830-4703-bf0e-562bf834a757">


### Contribution Guidelines
Contributions to improve the script's capabilities, Docker configurations, or documentation are encouraged! Fork the repository, make your modifications, and create a pull request.

### Issues
For any issues encountered or suggestions for enhancements, kindly open an issue on the repository. Feedback and contributions are highly valued.
