<template>
    <div class="e-shangpinban">
        <el-carousel indicator-position="outside" height="400px">
            <el-carousel-item v-for="item in items" :key="item" style="height: 400px">
                <div style="display: flex; justify-content: center; align-items: center">
                    <img :src="item" class="shangpin-image" />
                </div>
            </el-carousel-item>
        </el-carousel>
    </div>
</template>
<style type="text/scss" scoped lang="scss">
    .shangpin-image {
        object-fit: contain;
    }
</style>
<script>
    import { formatImageSrc } from "@/utils";

    export default {
        name: "e-shangpinban",
        data() {
            return {};
        },
        props: {
            images: String,
        },
        watch: {},
        computed: {
            items() {
                if (this.images) {
                    return this.images.split(",").map((s) => formatImageSrc(s));
                }
                return [];
            },
        },
    };
</script>
