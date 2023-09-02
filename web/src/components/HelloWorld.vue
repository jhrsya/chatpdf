
<template>
  <div class="app">
    
    <div class="upload-box">
      <input type="file" @change="uploadFile" accept=".pdf" />
      <div v-if="selectedFile">{{ selectedFile.name }}</div>
      <div v-else>点击选择PDF文件</div>
      <button @click="sendFileToServer">上传文件</button>
    </div>
    <div v-if="uploadStatus">{{ uploadStatus }}</div>
    <div class="conversation-box">
      <div class="messages" ref="messageContainer">
        <div v-for="message in messages" :key="message.id" class="message-wrapper">
          <div :class="['message', message.sender === 'user' ? 'user-message' : 'bot-message']">
            {{ message.text }}
          </div>
        </div>
      </div>
      <div class="input-box">
        <input type="text" v-model="newMessage" placeholder="在这里输入消息" @keydown.enter="sendMessage" />
        <button @click="sendMessage">发送</button>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'; // 引入axios

export default {
  data() {
    return {
      selectedFile: null,
      messages: [],
      newMessage: '',
      uploadStatus: ''
    };
  },
  methods: {
    uploadFile(event) {
      const file = event.target.files[0];
      this.selectedFile = file;
      // 在这里可以执行上传文件的操作，例如发送到服务器或进行其他处理
    },
    sendFileToServer() {
      if (this.selectedFile) {
        let formData = new FormData();
        formData.append("file", this.selectedFile);
        axios
          .post(`${process.env.VUE_APP_API_URL}/upload_files`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            // 处理服务器的响应
            if (response.data === 'upload success') {
              this.uploadStatus = '上传成功';
            } else if (response.data === 'upload failed') {
              this.uploadStatus = '上传失败';
            }
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
    sendMessage() {
      if (this.newMessage.trim() === '') {
        return; // 如果输入为空，则不发送消息
      }
      const userMessage = {
        id: Date.now(),
        sender: 'user',
        text: this.newMessage
      };
      this.messages.push(userMessage);
      this.newMessage = '';
      axios.post(`${process.env.VUE_APP_API_URL}/chat_file`, {
        message: userMessage.text
      })
      .then(response => {
        const botMessage = {
          id: Date.now() + 1,
          sender: 'bot',
          text: response.data
        };
        this.messages.push(botMessage);
      })
      .catch(error => {
        console.error(error);
      });
      this.scrollToBottom();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageContainer;
        container.scrollTop = container.scrollHeight;
      });
    }
  }
};
</script>


<style>
.app {
  display: flex;
  height: 100vh;
  flex-direction: row;
}

.upload-box {
  background-color: #f1f1f1;
  padding: 20px;
  width: 30%;
  margin-right: 20px;
}

.upload-box input[type="file"] {
  margin-bottom: 10px;
}

.conversation-box {
  background-color: #ffffff;
  padding: 20px;
  width: 70%;
}

.messages {
  height: 70%;
  overflow-y: auto;
}

.message-wrapper {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  margin-bottom: 10px;
  flex-direction: column;
}

.message {
  padding: 10px;
  border-radius: 5px;
  word-wrap: break-word;
  max-width: 80%;
}

.user-message {
  background-color: #c5e5ff;
  align-self: flex-end;
}

.bot-message {
  background-color: #f1f1f1;
  align-self: flex-start;
}

.input-box {
  display: flex;
  margin-top: 10px;
}

.input-box input {
  flex: 1;
  padding: 5px;
  margin-right: 10px;
}

.input-box button {
  padding: 5px 10px;
}
</style>


