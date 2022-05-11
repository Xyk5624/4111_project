<template>
  <div>
    <div class= "imagebar">
      <el-row :gutter="20">
        <el-col :span="4">
          <router-link to='/'>
            <img class="logo" src="../assets/EDG.jpg">
          </router-link>   
        </el-col>
        <div class="login-container">
          <el-col: span="6">
            Already have account?<router-link to='/login'>Sign in</router-link>
          </el-col:>
        </div>
      </el-row>     
    </div>
    <div class="register-container">
      <h1>Register</h1>
      <div class="input-container">
        <div style="float:left;">Email</div>
        <el-input v-model="form.email"></el-input>
        <div style="float:left; margin-top:10px;">Password</div>
        <el-input v-model="form.password"></el-input>
        <div style="float:left; margin-top:10px;">Username</div>
        <el-input v-model="form.username"></el-input>
        <div style="float:left; margin-top:10px;">Telephone</div>
        <el-input v-model="form.telephone"></el-input>
        <div style="float:left; margin-top:10px;">Apartment</div>
        <div style="clear:both;"></div>
        <el-select v-model="form.apartment" placeholder="Select" style="width: 100%; margin-top:10px;">
          <el-option
            v-for="(item,i) in apartments"
            :key="i"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>

        <div class="form-btns">
          <el-button type="primary" @click="onSubmit" class="submit-btn">Register   
          </el-button>
        </div>     
      </div>
    </div>
  
  

  </div>
</template>

<script>
import {sendPOST} from '../api/api.js';
import { ElMessage } from 'element-plus'
export default {
  name: 'register',
  data() {
      return {
          form: {
          email: '',
          password: '',
          username: '',
          telephone: '',
          apartment: ''
        },
        apartments: ["Hayden", "Enclave", "Jackson Park", "Eagle Lofts", "Coso Apartment", "1080 Amsterdam", "21 West End", "30 Morningside Drive", "Monarch Heights", "Hudson Park"]
      }
  },
  methods: {
    onSubmit() {
      var reg = /^[0-9a-zA-Z_.-]+[@][0-9a-zA-Z_.-]+([.][a-zA-Z]+){1,2}$/;
      if (!reg.test(this.form.email)) {
        alert("Please enter a valid email address.");
        return;
      }
      if (!this.form.password) {
        alert("Please enter a password.");
        return;
      }
      if (!this.form.username) {
        alert("Please enter a username.");
        return;
      }
      if (!this.form.telephone) {
        alert("Please enter a telephone.");
        return;
      }
      if (this.form.telephone < 1000000000 || this.form.telephone > 9999999999) {
        alert("Telephone number should be in range 1000000000-9999999999.");
        return;
      }
      if (!this.form.apartment) {
        alert("Please enter a apartment.");
        return;
      }
      var fd = new FormData();
      fd.append('email', this.form.email);
      fd.append('password', this.form.password);
      fd.append('username', this.form.username);
      fd.append('telephone', this.form.telephone);
      fd.append('apartment', this.form.apartment);
      sendPOST('/register', fd)
      .then((response) => {
        console.log(response);
        ElMessage({
          message: 'Register success.',
          type: 'success',
        })
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

.imagebar {
  height: 100px;
  border-bottom: 1px solid rgb(218, 218, 218);
}

.imagebar .logo {
  height: 100px;
  width: 100px;
  object-fit: cover;
}

.login-container {
  position: absolute;
  right: 0px;
  margin-top: 80px;
  text-align: right;
}

.register-container {
  margin:0 auto;
  width: 400px;
  text-align: center;
}

.input-container {
  width: 100%;
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