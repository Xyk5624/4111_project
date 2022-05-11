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
    <el-table :data="orders" style="width: 100%">
      <el-table-column prop="time" label="Time" min-width="20%" />
      <el-table-column label="Good" min-width="40%">
        <template #default="scope">
          <router-link :to="'/good/'+scope.row.good_id">
            <div>
              <img class="good_image" :src="url+scope.row.image_url">
              <div class="good_description">{{ scope.row.description }}</div>
            </div>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="price" label="Price" min-width="10%" />
      <el-table-column label="Review" min-width="20%">
        <template #default="scope">
          <a href="" @click.prevent="createReview(scope.row.good_id)">Review</a>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="dialogVisible" title="Write review to the seller" width="50%">
      <div class="input-container">
        <el-input
          v-model="reviewContent"
          :rows="2"
          type="textarea"
          placeholder="Please input review"
        />
        <div class="form-btns">
          <el-button type="primary" @click="reviewSubmit" class="submit-btn">Submit   
          </el-button>
        </div>  
      </div>
    </el-dialog>
  </div>      
</template>

<script>
import {sendPOST,sendGET} from '../api/api.js';
import config from '../config/config';
import headerbar from './headerbar.vue'
import { ElMessage } from 'element-plus'
export default {
  name: 'order',
  components: {headerbar},
  data() {
    return {
      orders: [],
      url: config.url,
      currentReview_goodId: "",
      dialogVisible: false,
      reviewContent: ""
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
    createReview(good_id) {
      this.dialogVisible = true;
      this.currentReview_goodId = good_id;
    },
    reviewSubmit() {
      var fd = new FormData();
      fd.append('content',this.reviewContent);
      fd.append('good_id',this.currentReview_goodId);
      sendPOST('/review',fd)
      .then(() => {
        ElMessage({
          message: 'Submit review success.',
          type: 'success',
        });
        this.dialogVisible = false;
        this.reviewContent = "";
      })
      .catch((error) => {
        alert(error);
      })
    }
  },
  created() {
    sendGET('/order')
      .then((response) => {
        this.orders = [];
         response.data.data.forEach((item) => {
            this.orders.push({
              good_id: item[0],
              price: item[1],
              time: item[2].slice(0,-4),
              image_url: item[3],
              description: item[4]
            })
          })
        console.log(this.orders);
      })
      .catch((error) => {
        alert(error);
      })
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

.good_image {
  display: inline-block;
  width: 100px;
  height: 100px;
  object-fit: cover;
  vertical-align: middle;
}

.good_description {
  display: inline-block;
  vertical-align: middle;
  margin-left: 20px;
  max-width: 50%;
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

