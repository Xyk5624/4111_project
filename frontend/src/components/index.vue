<template>
  <div class="index">
    <headerbar></headerbar>
    <div class="searchbar">
      <el-row :gutter="22">
        <el-col :span="2">
          <img class="logo" src="../assets/EDG.jpg">
        </el-col>
        <el-col :span="17" :offset="1">
          <div style="position: relative; top: 30px;">
            <el-input v-model="searchContent" placeholder="Search for second-handed goods">
              <template #prefix>
                <el-icon class="el-input__icon"><search /></el-icon>
              </template>
              <template #suffix style="position: relative; right:0;">
                <el-select v-model="searchCategory" placeholder="Select" 
                 :popper-append-to-body="false">
                  <el-option
                    v-for="(item,i) in categories"
                    :key="i"
                    :label="item"
                    :value="item"
                  >
                  </el-option>
                </el-select>
              </template>
            </el-input>
          </div>
        </el-col>
        <el-col :span="4">
          <div style="position: relative; top: 30px;">
            <el-button type="primary" style="width:100%" @click="submitSearch">Search</el-button>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="menubar">
      <el-menu
        :default-active="menuCategory"
        mode="horizontal"
        @select="handleSelect"
      >
        <el-menu-item
          v-for="(item,i) in categories"
          :index="item"
          :key="i"
        >{{item}}
        </el-menu-item>
      </el-menu>
    </div>
    <div class="main-container">
      <div class="left-container">
        <div style="margin-top: 20px;"></div>
        <el-switch
          v-model="sameBuilding"
          active-text="Goods in your building"
        >
        </el-switch>
        <div style="margin-top: 50px;">
          <div>
            <el-radio v-model="priceRange" label="0">All Price</el-radio>
          </div>
          <div>
            <el-radio v-model="priceRange" label="1">Price &lt; $20</el-radio>
          </div>
          <div>
            <el-radio v-model="priceRange" label="2">Price &gt;= $20</el-radio>
          </div>
        </div>
      </div>
      <div class="good-container">
        <div class="good" :key="i" v-for="(item,i) in goods">
          <router-link :to="'/good/'+item.good_id">
            <div>
              <img class="image" :src="url + item.imgurl">
            </div>
            {{item.description}}
          </router-link>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import headerbar from './headerbar.vue';
import config from '../config/config';
import {sendGET} from '../api/api.js';
import { ElMessage } from 'element-plus';
export default {
  components: { headerbar },
  name: 'index',
  props: {
    msg: String
  },
  data() {
    return {
      categories: ["All","Furniture","Electronic product","Book","Musical Instrument","Clothing",
      "Collection","Toy","Consumable","Transport","Ornament","Kitchenware"],
      searchCategory: "All",
      menuCategory: "All",
      goods: [],
      url: config.url,
      priceRange: "0",
      sameBuilding: false,
      searchContent: "",
    }
  },
  watch: {
    priceRange(){
      var data = this.makeData(this.menuCategory);
      sendGET('/good', data)
      .then((response) => {
        this.goods = response.data.data;
      })
      .catch((error) => {
        alert(error);
      })
    },
    sameBuilding() {
      if (this.sameBuilding == true){
        if (!this.$cookies.get('user_email')){
          ElMessage.error('Please sign in.');
          this.sameBuilding = false;
          return;
        }
      }
      var data = this.makeData(this.menuCategory);
      sendGET('/good', data)
      .then((response) => {
        this.goods = response.data.data;
      })
      .catch((error) => {
        alert(error);
      })
    },
  },
  methods: {
    makeData(category) {
      var data = {
        search: this.searchContent,
        category: category,
        price: this.priceRange
      };
      if (this.sameBuilding == true) {
        data.building = localStorage['building'];
      }
      return data;
    },
    handleSelect(selection) {
      this.menuCategory = selection;
      if (this.menuCategory != this.searchCategory){
        this.searchContent = "",
        this.searchCategory = "all"
      }
      var data = this.makeData(this.menuCategory);
      sendGET('/good', data)
      .then((response) => {
        this.goods = response.data.data;
      })
      .catch((error) => {
        alert(error);
      })
    },
    submitSearch() {
      var data = this.makeData(this.searchCategory);
      sendGET('/good', data)
      .then((response) => {
        this.goods = response.data.data;
        this.menuCategory = this.searchCategory;
      })
      .catch((error) => {
        alert(error);
      })
    },
  },
  created() {
    sendGET('/good')
    .then((response) => {
      this.goods = response.data.data;
    })
    .catch((error) => {
      alert(error);
    })
  }
}
</script>

<style scoped>
.searchbar {
  height: 100px;
  border-bottom: 1px solid rgb(218, 218, 218);
}

.searchbar .logo {
  height: 100px;
  width: 100px;
  object-fit: cover;
}

.main-container {
  display: flex;
}

.left-container {
  flex: 1;
  border-right: 1px solid rgb(218,218,218);
}

.good-container {
  flex: 8;
  display: flex;
  flex-wrap:wrap;
  /* justify-content: start; */
}

.good {
  width: 33%;
  height: 450px;
  text-align: center;
}

.image {
  margin-top: 20px;
  width: 80%;
  height: 380px;
}

/deep/.el-input__inner{
  border-color: black;
}

/deep/.el-input__suffix {
  right: 0;
}

/deep/.el-input__inner:focus, /deep/.el-input__inner:hover{
  border-color:black;
}

/deep/ .el-select .el-input .el-input__inner{
    border-color:black;
}

/deep/ .el-select .el-input.is-focus .el-input__inner{
    border-color:black;
}

/deep/ .el-menu--horizontal {
  justify-content: center;
}


/* /deep/ .myselect .el-select-dropdown__list{
  height: 1000px;
} */


/deep/ .el-select-dropdown__wrap {
  max-height: 500px;
}

</style>
