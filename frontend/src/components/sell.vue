<template>
  <div>
    <headerbar></headerbar>
    <div class="imagebar">
      <el-row :gutter="20">
        <el-col :span="4">
          <router-link to='/'>
            <img class="logo" src="../assets/EDG.jpg">
          </router-link>   
        </el-col>
      </el-row>
    </div>
    <div class="sell-container">
      <h1 style="font-size:40px">Sell your second-handed-good</h1>
      <div style="margin-top=40px;">
        <el-radio-group v-model="state" size="medium">
          <el-radio v-model="radio1" label="Sale">Sale</el-radio>
          <el-radio v-model="radio1" label="Auction">Auction</el-radio>
        </el-radio-group>
      </div>
      <div class="price-container" v-if="state == 'Sale'">
        <div style="font-size: 25px; margin:0 auto;">
        price($)
          <el-input v-model="price" style="width:25%; margin-left:10px;" placeholder="Please input price"></el-input>
        </div> 
      </div>
      <div class="price-container" v-else>
        <div style="margin:0 auto;">
        Start price($)
          <el-input v-model="price" style="width:30%; margin-left:10px;" placeholder="Please input price"></el-input>
        </div> 
        <!-- <div style="margin:0 auto; margin-top:25px;">
        Start time
          <el-date-picker
            v-model="start_time"
            type="datetime"
            placeholder="Select date and time"
          >
          </el-date-picker>
        </div> -->
        <div style="margin:0 auto; margin-top:25px;">
        Last hour
          <el-input v-model="count_down" style="width:30%; margin-left:10px;" placeholder="Please input length of aution"></el-input>
        </div>  
      </div>
      <div style="font-size: 25px;margin-top:10px;"> Category
        <el-select v-model="category" placeholder="Select" style="width: 24%; margin-top:10px; margin-left:10px;">
          <el-option
            v-for="(item,i) in categories"
            :key="i"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </div>
      <div class="price-container" style="margin-top:25px;margin-bottom: 20px;">
      Picture of the good
        <el-upload
          class="avatar-uploader"
          action=""
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
          :http-request="imgUpload"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><plus /></el-icon>
        </el-upload>
      </div>
      <div class="normal-container">Description</div>
      <div class="normal-container" style="margin-bottom: 50px;">
        <el-input v-model="description" size="medium" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" placeholder="Please Input" />
      </div>
      <div class="form-btns" style="margin-bottom: 150px;">
          <el-button type="primary" @click="onSubmit" class="submit-btn">Place Your Good in Market   
          </el-button>
        </div>  
    </div>
  </div>      
</template>

<script>
import {sendPOST} from '../api/api.js';
import { ElMessage } from 'element-plus'
import headerbar from './headerbar.vue'
export default {
  name: 'sell',
  components: {headerbar},
  data() {
    return {
      price: "",
      description: "",
      email: "",
      state: "Sale",
      start_time: "",
      count_down: "",
      imageUrl: "",
      mode: "",
      category: "",
      categories: ["Furniture", "Electronic product", "Book", "Musical Instrument", "Clothing", "Collection", "Toy", "Consumable", "Transport", "Ornament", "Kitchenware"]   
    }
  },
  methods: {
    onSubmit() {
      this.email = this.$cookies.get('user_email').replace(/"/g, "");
      var reg = /^[0-9a-zA-Z_.-]+[@][0-9a-zA-Z_.-]+([.][a-zA-Z]+){1,2}$/;
      if (!reg.test(this.email)) {
        alert("No user login.");
        return;
      }
      if (!this.state) {
        alert("Please choose between sell and auction.");
        return;
      }
      if (!this.price || this.price < 0) {
        alert("Please enter a price.");
        return;
      }
      if (this.state == 'auction') {
        if (!this.start_time) {
          alert("Please choose a start date.");
          return;
        }
        if (!this.count_down) {
          alert("Please enter how long auction will last.");
          return;
        }
      }
      if (!this.mode) {
        alert("Please choose a picture of your good.");
        return;
      } 
      if (!this.category) {
        alert("Please choose the category of the good.");
        return;
      } 
      if (!this.description) {
        alert("Please enter the description.");
        return;
      }     
      var fd = new FormData();
      fd.append('email',this.email);
      fd.append('state',this.state);
      fd.append('price',this.price);
      fd.append('category', this.category);
      if (this.state == "Auction") {
        fd.append('start_time',this.start_time);
        fd.append('count_down',this.count_down);
      }
      fd.append('description',this.description); 
      fd.append('file', this.mode)
      sendPOST('/sell',fd)
      .then((response) => {
        console.log(response);
        ElMessage({
          message: 'Put good in market success.',
          type: 'success',
        })
        this.$router.push('/');
      })
      .catch((error) => {
        alert(error);
      })
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    imgUpload(item) {
      this.mode = item.file;
      this.imageUrl = URL.createObjectURL(item.file)
      console.log(this.mode)
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

.sell-container {
  margin:0 auto;
  text-align: left;
}

.price-container {
  text-align: left;
  font-size: 25px;
}

.normal-container {
  margin-top:20px;
  width : 60%;
  font-size : 25px;
  text-align : left;
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
  width:40%;
  letter-spacing:0px;
  font-size: 20px!important;
}

/deep/ .avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
/deep/ .avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
/deep/.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 300px;
  height: 300px;
  text-align: center;
}
/deep/.avatar-uploader-icon svg {
  margin-top: 74px; /* (178px - 28px) / 2 - 1px */
}
.avatar {
  width: 300px;
  height: 300px;
  display: block;
}
</style>

