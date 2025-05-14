<template>
    <span class="e-select-view">{{content}}</span>
</template>
<style type="text/scss" lang="scss"></style>
<script>
    import DB from "@/utils/db";
    import { ElMessage } from "element-plus";

    export default {
        name: "e-select-view",
        data() {
            return {
                content: "",
                isLoading: false,
                retryCount: 0,
                maxRetries: 3
            };
        },
        props: {
            value: [String, Number],
            module: {
                type: String,
                required: true,
            },
            select: {
                type: [String, Number],
                required: true,
            },
            show: {
                type: [String, Number],
                required: true,
            },
        },
        watch: {
            value: {
                immediate: true,
                handler() {
                    this.getValue();
                }
            }
        },
        computed: {},
        methods: {
            getValue() {
                if (!this.value) {
                    this.content = "";
                    return;
                }
                DB.name(this.module)
                    .where(this.select, "=", this.value)
                    .select()
                    .then(res => {
                        if (res && res.length > 0 && res[0][this.show]) {
                            this.content = res[0][this.show];
                        } else {
                            this.content = "";
                        }
                    })
                    .catch(() => {
                        this.content = "";
                    });
            },
        },
        created() {
            this.getValue();
        },
        mounted() {},
        destroyed() {},
    };
</script>
