<template>
  <div>
    <el-row :gutter="20" v-if="cookie_email">
      <el-col :span="2">
        Hi <router-link :to="{path: '/profile/'+email_encoded}">{{username}}</router-link>
      </el-col>
      <el-col :span="2">
       <a href="" @click.prevent="signout">signout</a>
      </el-col>
      <el-col :span="2" :offset="11">
        <router-link to='/sell'>Sell Goods</router-link>
      </el-col>
      <el-col :span="2.1" >
        <router-link to='/auctions'>My Auctions</router-link>
      </el-col>
      <el-col :span="2">
        <router-link to='/soldgoods'>My Selling</router-link>
      </el-col>
      <el-col :span="2">
        <router-link to='/order'>My Order</router-link>
      </el-col>
    </el-row>
    <el-row :gutter="20" v-else>
      <el-col :span="4">
        <router-link to='/login'>Sign In</router-link> or
        <router-link to='/register'>Register</router-link>
      </el-col>
    </el-row>
    <div style="height:0; border-bottom: 1px solid rgb(218, 218, 218);"></div>
  </div>
</template>

<script>
import {sendDELETE} from '../api/api.js';
export default {
  name: 'headerbar',
  data() {
      return {
        cookie_email: this.$cookies.get('user_email')?this.$cookies.get('user_email').replace(/"/g, ""):null,
        email_encoded: this.$cookies.get('user_email')?
          encodeURIComponent(this.$cookies.get('user_email').replace(/"/g, "")):null,
        username: localStorage['username']
      }
  },
  methods: {
    signout() {
      sendDELETE('/signout')
      .then(()=>{
        localStorage.removeItem('username');
        this.$router.go(0);
      })
      .catch((error) => {
        alert(error);
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  color: blue;
  text-decoration: underline;
}
</style>

