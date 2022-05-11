<template>
  <div class="good">
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
    <div class="item">
      <el-row :gutter="20">
        <el-col :span="10">
          <img class="goodimage" :src="url + goods['image_url']">
        </el-col>
        <el-col :span="10">
          <div class="descrip">
            <h1 class="title">{{goods["description"]}}</h1>
            <el-descriptions style="font-size: 20px" :column="1" border>
              <el-descriptions-item label="Price">$ {{goods["price"]}}
              </el-descriptions-item>
              <el-descriptions-item label="State" >{{state}}
              </el-descriptions-item>
              <el-descriptions-item label="Sellers Email">
                <router-link :to="{path: '/profile/' + encoded_email}">{{goods["selleremail"]}}</router-link>
              </el-descriptions-item>
            </el-descriptions>
          </div>
          <div v-if="goods.selleremail != cookie_email">
            <el-button v-if="state == 'On Sale'" type="primary" @click="buyDialog=true" class="buyBtn">Buy now</el-button>
            <el-button v-if="state == 'Sold out'" type="info" disabled class="buyBtn">Sold out</el-button>
            <el-button v-if="state == 'On auction'" type="primary" @click="makeAuction" class="buyBtn">Auction now</el-button>
          </div>
          <div v-else>
            <el-button type="info" disabled class="buyBtn">It's your good</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
    <el-dialog
      v-model="buyDialog"
      title="Buy confirm"
      width="30%"
    >
      <span>Are you sure to buy this product?</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="buyDialog = false">Cancel</el-button>
          <el-button type="primary" @click="buy"
            >Confirm</el-button
          >
        </span>
      </template>
    </el-dialog>
    <el-dialog v-model="auctionDialog" title="Auction" width="40%">
      <div class="input-container">
        <el-descriptions style="font-size: 20px" :column="1">
              <el-descriptions-item label="Start Time: ">{{auctionInfo.start_time}}
              </el-descriptions-item>
              <el-descriptions-item label="End Time: " >{{auctionInfo.end_time}}
              </el-descriptions-item>
              <el-descriptions-item label="Current Max Price: " >${{auctionInfo.max_price}}
              </el-descriptions-item>
            </el-descriptions>
        <div style="float:left; margin-top:10px; margin-bottom:10px;font-size:20px">Your price</div>
        <el-input v-model="auction_price"></el-input>
        <div style="clear:both;"></div>
        <div class="form-btns">
          <el-button type="primary" @click="priceSubmit" class="submit-btn">Offer price   
          </el-button>
        </div>  
      </div>
    </el-dialog>
  </div>
</template>

<script>
import headerbar from './headerbar.vue'
import config from '../config/config';
import {sendGET,sendPOST} from '../api/api.js';
import { ElMessage } from 'element-plus'
export default {
    components: {headerbar},
    name: 'good',
    props: {
      msg: String
    },
    data() {
      return {
        good_id: this.$route.params.id,
        url: config.url,
        goods: {},
        state: 'none',
        encoded_email: "",
        buyDialog: false,
        auctionDialog: false,
        cookie_email: this.$cookies.get('user_email')?this.$cookies.get('user_email').replace(/"/g, ""):null,
        auction_price: 0,
        auctionInfo: {},
      }
    },
    methods: {
      buy() {
        if (!this.cookie_email) {
          ElMessage.error('Please sign in.')
          this.$router.push('/login');
          return
        }
        var fd = new FormData();
        fd.append('good_id',this.good_id);
        fd.append('price',this.goods['price']);
        sendPOST('/buy',fd)
        .then(() => {
          ElMessage({
            message: 'Success.',
            type: 'success',
          })
          this.buy = false;
          this.$router.go(0);
        })
        .catch((error) => {
          alert(error.response.data.message);
        })
      },
      makeAuction() {
        if (!this.cookie_email) {
          ElMessage.error('Please sign in.')
          this.$router.push('/login');
          return
        }
        this.auctionDialog = true;
        sendGET('/auction',{'good_id':this.good_id})
        .then((response) => {
          this.auctionInfo.max_price = response.data.data[0]
          this.auctionInfo.start_time = response.data.data[1].slice(0,-4)
          this.auctionInfo.end_time = response.data.data[2].slice(0,-4)
        })
        .catch((error) => {
          alert(error.response.data.message);
        })
      },
      priceSubmit() {
        if (this.auction_price <= this.auctionInfo.max_price) {
          ElMessage.error('Your price must be higher than the current price')
          return
        }
        var fd = new FormData();
        fd.append('good_id',this.good_id);
        fd.append('offerprice',this.auction_price);
        sendPOST('/auction',fd)
        .then(() => {
          ElMessage({
            message: 'Success.',
            type: 'success',
          })
          this.auctionDialog = false;
          this.$router.go(0);
        })
        .catch((error) => {
          alert(error.response.data.message);
        })
      }
    },
    created() {
      sendGET('/good', {"good_id":this.good_id})
      .then((response) => {
        this.goods = response.data.data;
        if (this.goods["state"] == 1) {this.state = 'On Sale';}
        else if (this.goods["state"] == 2) {this.state = 'On auction';}
        else if (this.goods["state"] == 3) {this.state = 'Sold out';}
        else if (this.goods["state"] == 4) {this.state = 'Off-shelf';}
        this.encoded_email = encodeURIComponent(this.goods["selleremail"].replace(/"/g, ""))
        console.log(this.goods);
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

.item {
  height: 500px;
  width: 100%;
}

.goodimage {
  width: 100%;
  height: 700px;
  margin-top : 70px;
}

.descrip {
  width: 100%;
  margin-top : 70px;
  margin-left : 20%;
  font-size: large;
}

.descrip .title {
  text-align: center;
}

.buyBtn {
  width: 50%;
  height: 10%;
  margin-top : 70px;
  margin-left : 45%;
  border-radius: 50px;
  font-size: 30px;
}

.submit-btn {
  margin-top : 20px;
}

</style>