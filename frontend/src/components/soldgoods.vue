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
    <el-table :data="goods" style="width: 100%;font-size: 22px">     
      <el-table-column label="Good" min-width="38%">
        <template #default="scope">
          <router-link :to="'/good/'+scope.row.good_id">
            <div>
              <img class="good_image" :src="url+scope.row.image_url">
              <div class="good_description">{{ scope.row.description }}</div>
            </div>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="price" label="Price" min-width="10%" align="center"/>
      <el-table-column label="State" min-width="10%" align="center">
        <template #default="scope">
          <span v-if="scope.row.state=='1'">On Sale</span>
          <span v-if="scope.row.state=='2'">On Auction</span>
          <span v-if="scope.row.state=='3'">Sold Out</span>
          <span v-if="scope.row.state=='4'">Off Shelf</span>
        </template>
      </el-table-column>
      <el-table-column label="Choice" min-width="25%" align="center">
        <template #default="scope">
          <span v-if="scope.row.state=='1' || scope.row.state=='2'">
            <el-button style="width=100%" type="danger" @click="onSubmit(scope.row)" class="submit-btn">Off-shelf goods    
            </el-button> 
          </span>
          <span v-else>
            <el-button style="width=100%" type="danger" @click="onSubmit" class="submit-btn" disabled>Off-shelf goods    
            </el-button> 
          </span>
        </template>      
      </el-table-column>
    </el-table>
  </div>      
</template>

<script>
import {sendGET, sendPOST} from '../api/api.js';
import config from '../config/config';
import { ElMessage } from 'element-plus'
import headerbar from './headerbar.vue'
export default {
  name: 'order',
  components: {headerbar},
  data() {
    return {
      url: config.url,
      goods: [],
    }
  },
  methods: {
    onSubmit(good) {
      var fd = new FormData();
      fd.append('state', good.state);
      fd.append('good_id', good.good_id);
      sendPOST('/offshelf', fd)
      .then((response) => {
        console.log(response);
        ElMessage({
          message: 'Off shelf success.',
          type: 'success',
        })
        this.$router.go(0);
      })
      .catch((error) => {
        alert(error);
      })
    },
  },
  created() {
    sendGET('/soldgoods')
      .then((response) => {
        this.goods = [];
        response.data.data.forEach((item) => {
            this.goods.push({
                state: item.state,
                price: item.price,
                description: item.description,
                image_url: item.image_url,
                good_id: item.good_id,
            })
            console.log(item.good_id);
        })
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

.submit-btn {
  width:50%;
  letter-spacing:0px;
  font-size: 20px!important;
}
</style>

