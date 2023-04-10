import React, { useState, useEffect } from 'react';
import './ChatApp.css';
import userAvatar from './user-avatar.png';
import botAvatar from './bot-avatar.jpeg';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faUpload } from '@fortawesome/free-solid-svg-icons';


const ChatApp = () => {
  const [newMessage, setNewMessage] = useState('');
  const [image, setImage] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [prompt, setPrompt] = useState('');
  const [link, setLink] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userResponse, setuserResponse] = useState('prompt');
  const [userInput, setUserInput] = useState('');
  const [category, setCategory] = useState('');
  const [pdfBlob, setPdfBlob] = useState(null);

  const fakeMessages = [
    { id: 1, text: 'Hi there! What can I do for you', sender: 'bot', avatar: botAvatar },
    // { id: 2, text: 'Hi there!', sender: 'bot', avatar: botAvatar },
    // { id: 3, text: 'What can I do for you?', sender: 'bot', avatar: botAvatar },
    // { id: 4, text: "Can you summarize this Medium blog for me?", sender: 'user', avatar: userAvatar },
    // { id: 5, text: 'Sure, Please enter the URL for the blog.', sender: 'bot', avatar: botAvatar },
    // { id: 6, text: "MEDIUM_LINK: https://medium.com/sfu-cspmp/the-artistic-potential-of-ai-understanding-dall-e-2-and-stable-diffusion-10a82e6965c0", sender: 'user', avatar: userAvatar },
    // { id: 7, text: '<div class="title">The Artistic Potential of AI: Understanding DALL-E 2 and Stable Diffusion</div><div class="sub-title">Written by Machine Minds on Feb 11</div><div class="heading">An Overview</div><div>AI is transforming the digital world by allowing machines to act and think like humans. Generative AI takes this a step further, introducing the ability to craete visuals, texts, sounds or songs. Models such as DALL-E 2 and Stable Diffusion, developed by OpenAI and LMU Munich respectively, use transformer-based designs and extensive training data to generate images from verbal descriptions, pushing the boundaries of creativity. AI has something to offer for everyone, with endless possibilities in store.<div>  \n <div class="heading">The Technology Behind DALL-E 2 </div>', sender: 'bot', avatar: botAvatar },
  ];
  const [messages, setMessages] = useState(fakeMessages);
  // This useEffect hook will simulate fetching messages from a backend.
  // useEffect(() => {
    
  //   const fetchMessages = async () => {
  //     // Fetch messages from the API
  //       var requestOptions = {
  //         method: 'GET',
  //         redirect: 'follow'
  //       };
  //     fetch(`http://13.58.199.27:8000/model_switcher_test/?prompt=Can you summarize this Medium blog for me?&medium_link=https://medium.com/sfu-cspmp/the-artistic-potential-of-ai-understanding-dall-e-2-and-stable-diffusion-10a82e6965c0`, requestOptions)
  //         .then(response => response.text())
  //         .then(results => {
  //           console.log(results);
  //           let jsonObject = JSON.parse(results)
  //           console.log(jsonObject);
  //           setMessages(prevMessages => [
  //             ...prevMessages,
  //             { id: prevMessages.length + 1, text: jsonObject['summary'], sender: 'bot', avatar: botAvatar }
  //           ]);
  //           // fakeMessages.push({id: fakeMessages.length + 1, text: jsonObject['summary'], sender: 'bot', avatar: botAvatar})
            
  //         })
  //         .catch(error => console.log('Failed to fetch messages', error))
  //         .finally(() => {
  //           setIsLoading(false)
  //         })
  //   };

  //   fetchMessages();
  // }, []);

  const handleSubmit = (event, e) => {
    event.preventDefault();
    console.log(image);
    if (newMessage.trim()) {
      const newMessageObj = {
        id: messages.length + 1,
        text: newMessage,
        sender: 'user',
        avatar: userAvatar,
      };
    }
      var fileBuffer = null;
      // if (image) {
      //   setMessages(prevMessages => [
      //     ...prevMessages,
      //     { id: prevMessages.length + 1, image: URL.createObjectURL(image), sender: 'user', avatar: userAvatar }
      //   ]);
      //   file = image;
      //   setImage(null);
      //   setUploadedFileName('');
      // }
      let file = {...image};
      if (image) {
     
        // const reader = new FileReader();
        // reader.onload = (event) => {
        //   console.log(event)
        //   const arrayBuffer = event.target.result;
        //   blob = new Blob([arrayBuffer], { type: 'application/pdf' });
        //   setMessages(prevMessages => [
        //     ...prevMessages,
        //     { id: prevMessages.length + 1, file: blob, sender: 'user', avatar: userAvatar }
        //   ]);
        // };
        // file = blob;
        // reader.readAsArrayBuffer(image);
        //  setImage(null);
        // setUploadedFileName('');
      
      setMessages(prevMessages => [
        ...prevMessages,
        { id: prevMessages.length + 1, text: image.name, sender: 'user', avatar: userAvatar }
      ]);
      }
      else{
        setMessages(prevMessages => [
          ...prevMessages,
          { id: prevMessages.length + 1, text: newMessage, sender: 'user', avatar: userAvatar }
        ]);
      }
      // setMessages([...messages, newMessageObj]);
      let shouldUpdateState = false;
      let jsonObject = {};
      if(userResponse == 'prompt'){
        setIsLoading(true);
        var requestOptions = {
          method: 'GET',
          redirect: 'follow'
        };
        fetch(`http://3.14.131.137:8000/model_get_category/?prompt=${newMessage}`, requestOptions)
          .then(response => response.text())
          .then(result => {
            console.log(result);
            jsonObject = JSON.parse(result);
            shouldUpdateState = true;
          })
          .catch(error => console.log('error', error))
          .finally(() => {
            if(shouldUpdateState){
              // setUserInput(category);
              setCategory(jsonObject['category']);
              let msg = '';
              setIsLoading(false);
              switch(jsonObject['category']) {
                case 'blog':
                  msg = 'Sure! Can you provide the link for the blog?';
                  setuserResponse('input');
                  break;
                case 'resume':
                  msg = 'Sure! Can you provide the pdf file for your resume?';
                  setuserResponse('input');
                  break;
                  case 'suduko':
                    msg = 'Sure! Can you provide the image for your suduko puzzle?';
                    setuserResponse('input');
                    break;
                    case 'audio_to_text':
                      msg = 'Sure! Can you provide the audio with .wav extension?';
                      setuserResponse('input');
                      break;
                    default:
                      msg = 'Sorry, I am not sure. Could you please provide another prompt?';
                      setuserResponse('prompt');
              }
              setMessages(prevMessages => [
                ...prevMessages,
                { id: prevMessages.length + 1, text: msg, sender: 'bot', avatar: botAvatar }
              ]);
            }
          });
      }
      if(userResponse === 'input'){
        setIsLoading(true);
        let url = '';
        let res = '';
        let formdata = new FormData();
        switch(category) {
          case "blog":
            formdata.append("medium_link", newMessage);
            console.log(formdata)
            url = 'http://3.14.131.137:8000/model_get_blog_summary/'
            break;
          case "resume":
            console.log('blob', pdfBlob, image);

            formdata.append("resume",  image, "sample_resume.pdf");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_resume_summary/";
            break;
            case "resume":

            formdata.append("resume",  image, "sample_resume.pdf");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_resume_summary/";
            break;
            case "suduko":

            formdata.append("suduko",  image, "sample_sudoku.jpeg");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_suduko/";
            break;
            case "audio_to_text":

            formdata.append("audio",  image, "audio.wav");
            console.log('form',formdata);
            url = "http://3.14.131.137:8000/model_get_audio_to_text/";
            break;
        }
        let requestOptions = {
          method: 'POST',
          body: formdata,
          redirect: 'follow'
        };
        fetch(`${url}`, requestOptions)
          .then(response => response.text())
          .then(result => {
            console.log(result);
            let jsonObject = JSON.parse(result);
            if(category === "audio_to_text"){
              res = jsonObject['transcript']
            }
            else{
              res = jsonObject['summary']
            }
            shouldUpdateState = true;
          })
          .catch(error => console.log('error', error))
          .finally(() => {
            if(shouldUpdateState){
              // setUserInput(category);
              setIsLoading(false);
                  setMessages(prevMessages => [
                    ...prevMessages,
                    { id: prevMessages.length + 1, text: res, sender: 'bot', avatar: botAvatar },
                    { id: prevMessages.length + 2, text: "What else I can do for you?", sender: 'bot', avatar: botAvatar }
                  ]);
                  setuserResponse('prompt');
            }
             setImage(null);
        setUploadedFileName('');
          });
       
      }
      setNewMessage('');
      // setTimeout(() => {
      //   setMessages(prevMessages => [
      //     ...prevMessages,
      //     { id: prevMessages.length + 1, text: "Sorry, I don't understand. Could you please rephrase that?", sender: 'bot', avatar: botAvatar }
      //   ]);
      // }, 1000);
    // }
  };

    

  const handleFileInputChange = (event) => {
    console.log(event.target.files)
    setImage(event.target.files[0]);
    setUploadedFileName(event.target.files[0].name);
  //   if(category === "resume"){
  //     const file = event.target.files[0];
  //   const reader = new FileReader();

  //   reader.onload = () => {
  //     const pdfDataUrl = reader.result;
  //     const pdfBlob = new Blob([pdfDataUrl], { type: 'application/pdf' });
  //     setPdfBlob(pdfBlob);
  //   }
  //   reader.readAsArrayBuffer(file);
  //   }
  //  else if(category === "suduko"){

  //   }
    
  };

  return (
    <div className="chat-container">
      <div className='header'>
      <div style={{color: '#fff', padding:'10px', fontSize: "32px", fontWeight: 'bold'}}>OmniBot</div>
      </div>
      <div className="message-container">
        {messages.map((message) => (
          <div>
          <div key={message.id} className={`message ${message.sender}`}>
            <img src={message.avatar} alt="Avatar" className="avatar" />
            <div className="message-content">
              {message.text && <div style={{whiteSpace: 'pre-line', verticalAlign: 'bottom'}} dangerouslySetInnerHTML={{__html:message.text}}></div>}
              {message.image && <img src={message.image} alt="User uploaded" />}
            </div>
          </div>
          </div>
        ))}
        <div>
          {isLoading ? (
            // Show loader while data is being fetched
            <div className='loading' style={{ display: 'flex', alignItems: 'center' }}><img src={botAvatar} alt="Avatar" className="avatar" /> is typing...</div>
          ) : null}</div>
      </div>
      <div className='footer'>
      <form onSubmit={handleSubmit}>
  <input
    type="text"
    placeholder={uploadedFileName ? uploadedFileName : 'Type your message...'}
    value={newMessage}
    onChange={(event) => setNewMessage(event.target.value)}
    style={{ width: '300px' }}
  />
  <label htmlFor="file-input">
    <FontAwesomeIcon icon={faUpload} style={{ color: '#376B7E', margin: '8px' }} />
  </label>
  <input
    id="file-input"
    type="file"
    accept="application/pdf, image/*, audio/wav"
    onChange={handleFileInputChange}
    style={{ display: 'none' }}
  />
  <button type="submit">
    <FontAwesomeIcon icon={faPaperPlane} style={{ color: 'white' }} />
  </button>
</form>
</div>
</div>
  );
};

export default ChatApp;
