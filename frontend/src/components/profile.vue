<template>
  <div>
    <headerbar />
    <div class="imagebar">
      <el-row :gutter="20">
        <el-col :span="4">
          <router-link to='/'>
            <img class="logo" src="../assets/EDG.jpg">
          </router-link>   
        </el-col>
      </el-row>
    </div>
    <div class="profile-container">
      <h1>{{userinfo.username}}</h1>
      <div class="separate-line"></div>
      <h2 class="h2class">User info</h2>
      <span style="position: relative; bottom: 10px; margin-left: 20px;" v-if="email_param == cookie_email">
        <el-button circle @click="dialogVisible = true"><el-icon><edit></edit></el-icon></el-button>
      </span>
      <el-descriptions :column="1" style="font-size: 20px">
        <el-descriptions-item label="Email:">{{userinfo.email}}</el-descriptions-item>
        <el-descriptions-item label="Telephone:">{{userinfo.telephone}}</el-descriptions-item>
        <el-descriptions-item label="Building:">{{userinfo.building_name}}</el-descriptions-item>
        <el-descriptions-item label="Address:">{{userinfo.address}}</el-descriptions-item>
        <el-descriptions-item label="Zip_code:">{{userinfo.zip_code}}</el-descriptions-item>
      </el-descriptions>
      <div class="separate-line"></div>
      <h2>Reviews</h2>
      <div class="review-container" :key="i" v-for="(item,i) in reviews">
        <div class="review-left-container">By <router-link 
        :to="'/profile/'+encodeURIComponent(item.sender_email)">{{item.sender}}</router-link><br>
        {{item.time}}
        </div>
        <div class="review-right-container">{{item.content}}</div>
      </div>
    </div>
    <el-dialog v-model="dialogVisible" title="Edit user info" width="30%">
      <div class="input-container">
        <div style="float:left; margin-top:10px;">Telephone</div>
        <el-input v-model="editform.telephone"></el-input>
        <div style="float:left; margin-top:10px;">Apartment</div>
        <div style="clear:both;"></div>
        <el-select v-model="editform.building_name" placeholder="Select" style="width: 100%; margin-top:10px;">
          <el-option
            v-for="(item,i) in apartments"
            :key="i"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
        <div class="form-btns">
          <el-button type="primary" @click="editSubmit" class="submit-btn">Edit   
          </el-button>
        </div>  
      </div>
    </el-dialog>
  </div>      
</template>

<script>
import headerbar from './headerbar.vue'
import {sendPOST,sendGET} from '../api/api.js';
import { ElMessage } from 'element-plus'
export default {
  name: 'profile',
  components: { headerbar },
  data() {
    return {
      cookie_email: this.$cookies.get('user_email')?this.$cookies.get('user_email').replace(/"/g, ""):null,
      email_param: this.$route.params.email,
      dialogVisible: false,
      userinfo: {},
      editform: {},
      reviews: [],
      apartments: ["Hayden", "Enclave", "Jackson Park", "Eagle Lofts", "Coso Apartment", "1080 Amsterdam", "21 West End", "30 Morningside Drive", "Monarch Heights", "Hudson Park"],
    }
  },
  methods: {
    editSubmit() {
      if (this.editform.telephone.length != 10) {
        console.log(this.editform.telephone);
        ElMessage.error('Telephone must be 10 digits');
        return;
      }
      var fd = new FormData();
      fd.append('telephone',this.editform.telephone);
      fd.append('building_name',this.editform.building_name);
      sendPOST('/user',fd)
      .then((response) => {
        ElMessage({
          message: 'Edit success.',
          type: 'success',
        })
        this.dialogVisible = false;
        this.userinfo.telephone = this.editform.telephone;
        this.userinfo.building_name = this.editform.building_name;
        this.userinfo.address = response.data.data.address;
        this.userinfo.zip_code = response.data.data.zip_code;
        localStorage["building"]= this.editform.building_name;
      })
      .catch((error) => {
        alert(error);
      })
    },
    fetchUser() {
      sendGET('/user',{email:this.email_param})
      .then((response)=>{
        this.userinfo.username = response.data.data[0];
        this.userinfo.email = response.data.data[1];
        this.userinfo.telephone = response.data.data[2].toString();
        this.userinfo.building_name = response.data.data[3];
        this.userinfo.address = response.data.data[4];
        this.userinfo.zip_code = response.data.data[5];
        this.editform.telephone = this.userinfo.telephone
        this.editform.building_name = this.userinfo.building_name
        sendGET('/review',{receiver:this.email_param})
        .then((response)=>{
          this.reviews = []
          response.data.data.forEach((item) => {
            this.reviews.push({
              content: item[0],
              time: item[1].slice(0,-4),
              sender_email: item[2],
              sender: item[3]
            })
          })
        })
        .catch((error)=>{
          console.log(error);
        })
      })
      .catch((error)=>{
        console.log(error);
      })
    }
  },
  created() {
    this.fetchUser();
  },
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

.profile-container {
  margin-top: 50px;
}

.h2class {
  display: inline;
}

.separate-line {
  width: 80%;
  border-bottom: 1px solid rgb(218,218,218);
  margin-bottom: 20px;
}

.review-container {
  display: flex;
  height: 100px;
  width: 80%;
}

.review-left-container {
  flex: 3;
}

.review-right-container {
  flex: 7;
}

.input-container {
  width: 70%;
  margin: 0 auto;
}

.form-btns {
  margin-top: 20px;
  text-align: center;
}
</style>

