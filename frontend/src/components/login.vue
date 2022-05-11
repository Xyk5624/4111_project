<template>
  <div class="login-container">
      <router-link to='/'>
        <img class="logo" src="../assets/EDG.jpg">
      </router-link> 
      <div class="input-container">
        <h1>Sign in</h1>
        <div style="float:left;">Email</div>
        <el-input v-model="form.email"></el-input>
        <div style="float:left; margin-top:10px;">Password</div>
        <el-input type="password" 
          v-model="form.password" @keyup.enter="onSubmit"></el-input>
        <div class="form-btns">
          <el-button type="primary" @click="onSubmit" class="submit-btn">Sign-in</el-button>
        </div>           
      </div>
  </div>      
</template>

<script>
import {sendPOST} from '../api/api.js';
export default {
  name: 'login',
  data() {
    return {
      form: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit() {
      var fd = new FormData();
      fd.append('email',this.form.email);
      fd.append('password',this.form.password);
      sendPOST('/login',fd)
      .then((response) => {
        localStorage["username"]=response.data.data.username;
        localStorage["building"]=response.data.data.building;
        this.$router.push('/');
      })
      .catch((error) => {
        alert(error);
      })
    },
  }
}
</script>

<style scoped>
body {
  font-family: Helvetica, sans-serif;
}
.login-container {
  margin:0 auto;
  width: 400px;
  text-align: center;
}

.input-container {
  width: 80%;
  margin: 0 auto;
  border: 1px solid rgb(218,218,218);
  border-radius: 5px;
  padding: 20px;
}

.form-btns {
  margin-top: 20px;
}

.submit-btn {
  width:100%;
  letter-spacing:0px;
  font-size: 20px!important;
}
</style>

