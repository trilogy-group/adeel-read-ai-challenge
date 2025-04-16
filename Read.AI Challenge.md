### **Purpose**

Create a tool that converts meeting data from Read.ai into structured document formats (.PDF and .MD) containing meeting details, summary, and synchronized transcript.

### **Timeline**

Complete this challenge within 24 hours after receiving it.

### [**Input Files**](https://drive.google.com/drive/folders/1_jIGaEYMOCqnb8ZSd2Ol1vWXV1_2yDgh)

* `raw_Event.json` \- The Read.ai payload for the meeting event  
* `Meet Meeting Transcript.txt` \- Transcript file from Read.ai  
* `Meet Meeting Recording.mp4` \- The video recording of the meeting

  ### **Output Requirements**

1. Generate both PDF and Markdown versions of the meeting documentation  
2. Each document must include:  
   * Meeting details (title, date, participants, duration)  
   * Meeting summary  
   * Full transcript with timestamps  
3. The transcript timestamps must be formatted as "minutes  
    from meeting start"  
4. Timestamps in the transcript must synchronize with the video recording

   ### **Technical Requirements**

1. Create a modular and maintainable codebase that can process various meeting inputs  
2. Include appropriate error handling for missing or malformed input files  
3. Provide clear documentation on how to use the tool

   ### **Video Demo Requirement**

Create a narrated video demo (maximum 5 minutes) that includes:

1. Explanation of your code structure and key components  
2. Overview of the input files and their format  
3. Live demonstration of running your command/tool  
4. Explanation of the output files generated  
5. Any challenges you faced and how you solved them

   ### **Approach**

We encourage an AI-first approach to this challenge. Feel free to leverage AI tools to help you with coding, debugging, and documentation. This is an opportunity to demonstrate how you can effectively use AI to solve problems efficiently.

### **General Guidance**

If any part of this challenge is not crystal clear, please add a comment to that section in your PR and tag @lmrlima so I can view and answer your question. Don't make assumptions about unclear requirements \- it's better to ask for clarification.

### **Submission Guidelines**

1. Create a new GitHub repository for this project  
2. Use meaningful commit messages that show your development process  
3. Include a README.md with:  
   * Setup instructions  
   * Usage examples  
   * Brief explanation of your approach (including how you leveraged AI tools)  
4. Create a pull request to the main branch  
5. Share your GitHub repository with GitHub user "lmrlima"  
6. Include a link to your video demo in the README and PR description

   ### **Evaluation Criteria**

Your submission will be evaluated on:

1. Code quality and organization  
2. Accuracy of timestamp synchronization  
3. Error handling and edge cases  
4. Documentation clarity  
5. Effective use of AI tools to accelerate development  
6. Clarity and completeness of your video demonstration

