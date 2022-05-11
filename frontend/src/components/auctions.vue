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
    <el-table :data="goods" style="width: 100%">     
      <el-table-column label="Good" min-width="32%">
        <template #default="scope">
          <router-link :to="'/good/'+scope.row.good_id">
            <div>
              <img class="good_image" :src="url+scope.row.image_url">
              <div class="good_description">{{ scope.row.description }}</div>
            </div>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="offer_price" label="My Price" min-width="13%" />
      <el-table-column prop="maxprice" label="Max Price" min-width="13%" />
      <el-table-column prop="start_time" label="Start Date" min-width="23%" />
      <el-table-column prop="count_down" label="End Date" min-width="17%" />
    </el-table>
  </div>      
</template>

<script>
import {sendGET} from '../api/api.js';
import config from '../config/config';
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
  created() {
    sendGET('/auctions')
      .then((response) => {
        this.goods = [];
        response.data.data.forEach((item) => {
            this.goods.push({
                maxprice: item.maxprice,
                offer_price: item.offer_price,
                description: item.description,
                image_url: item.image_url,
                start_time: item.start_time,
                count_down: item.count_down,
                good_id: item.good_id,
            })
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
</style>

