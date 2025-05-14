import http, { fetchPostJson } from "./ajax/http";
import config from "@/config";
import { ref } from "vue";
import { ElMessage } from "element-plus";

export class Query {
    constructor(name) {
        this.name = name;
        this.options = {};
    }

    where(field, exp, condition) {
        if (!this.options.where) {
            this.options.where = [];
        }
        var len = arguments.length;
        if (len == 1) {
            this.options.where.push({ raw: true, name: field });
            return this;
        }
        if (len == 2) {
            condition = exp;
            exp = "=";
        }
        this.options.where.push({
            name: field,
            exp: exp,
            value: condition,
        });
        return this;
    }

    executeQuery(func, args) {
        if (!this.name || !func) {
            return Promise.reject(new Error('必须提供表名和方法名'));
        }
        
        // 构建请求数据
        const data = {
            name: this.name,
            func: func,
            where: this.options.where || '',
            order: this.options.order || '',
            field: this.options.field || '',
            args: args || null
        };
        
        // 特殊处理 limit 参数
        if (this.options.limit) {
            // 如果是数字，直接使用
            if (typeof this.options.limit === 'number') {
                data.limit = this.options.limit;
            } 
            // 如果是字符串，检查是否可以转换为数字
            else if (typeof this.options.limit === 'string' && !isNaN(parseInt(this.options.limit))) {
                data.limit = parseInt(this.options.limit);
            }
            // 否则使用原始对象
            else {
                data.limit = this.options.limit;
            }
        } else {
            data.limit = '';
        }
        
        console.log('executeQuerydata - 数据对象:', data);
        const jsonData = JSON.stringify(data);
        console.log('executeQuerydata - JSON字符串:', jsonData);
        
        // 使用 XMLHttpRequest 发送请求 - 尝试两种不同的方式
        return new Promise((resolve, reject) => {
            // 尝试第一种方式：使用 FormData
            const xhr = new XMLHttpRequest();
            const url = config.service_url + config.query_url;
            
            console.log('请求URL:', url);
            
            xhr.open('POST', url, true);
            // 不要设置 Content-Type，让浏览器自动设置
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.withCredentials = true;
            
            xhr.onload = function() {
                console.log('响应状态码:', xhr.status);
                console.log('响应头:', xhr.getAllResponseHeaders());
                console.log('响应内容:', xhr.responseText);
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        console.log('解析后的响应:', response);
                        
                        // 检查响应状态
                        if (response.code === 0) {
                            // 成功响应
                            // 检查数据格式，处理可能的嵌套结构
                            if (response.data && typeof response.data === 'object') {
                                if ('data' in response.data) {
                                    // 嵌套数据结构 {data: {data: [...], total: ...}}
                                    console.log('找到嵌套数据结构, 返回 response.data.data:', response.data.data);
                                    // 保留元数据（例如 total）用于分页
                                    const result = response.data.data;
                                    // 添加元数据属性
                                    if ('total' in response.data) {
                                        Object.defineProperty(result, '_total', {
                                            value: response.data.total,
                                            enumerable: false
                                        });
                                    }
                                    if ('page' in response.data) {
                                        Object.defineProperty(result, '_page', {
                                            value: response.data.page,
                                            enumerable: false
                                        });
                                    }
                                    if ('limit' in response.data) {
                                        Object.defineProperty(result, '_limit', {
                                            value: response.data.limit,
                                            enumerable: false
                                        });
                                    }
                                    resolve(result);
                                } else {
                                    // 直接数据结构 {data: [...]}
                                    console.log('找到直接数据结构, 返回 response.data:', response.data);
                                    resolve(response.data);
                                }
                            } else {
                                // 如果 data 不是对象或为 null，则直接返回
                                console.log('数据不是对象，直接返回 response.data:', response.data);
                                resolve(response.data);
                            }
                        } else {
                            // 错误响应
                            console.error('服务器返回错误:', response.msg);
                            reject(new Error(response.msg || '请求失败'));
                        }
                    } catch (e) {
                        console.error('解析响应失败:', e);
                        reject(e);
                    }
                } else {
                    console.error('请求失败, 状态码:', xhr.status);
                    reject(new Error(`请求失败，状态码: ${xhr.status}`));
                }
            };
            
            xhr.onerror = function(error) {
                console.error('请求出错:', error);
                reject(new Error('请求发送失败'));
            };
            
            xhr.onreadystatechange = function() {
                console.log('请求状态变化:', xhr.readyState);
            };
            
            // 使用 FormData 发送数据
            const formData = new FormData();
            
            // 添加基本参数
            formData.append('name', this.name);
            formData.append('func', func);
            
            // 处理 where 参数
            if (this.options.where) {
                // 如果是数组或对象，转换为JSON字符串
                if (typeof this.options.where === 'object') {
                    formData.append('where', JSON.stringify(this.options.where));
                } else {
                    formData.append('where', this.options.where);
                }
            } else {
                formData.append('where', '');
            }
            
            // 处理 order 参数
            if (this.options.order) {
                // 如果是数组，转换为JSON字符串
                if (Array.isArray(this.options.order)) {
                    formData.append('order', JSON.stringify(this.options.order));
                } else {
                    formData.append('order', this.options.order);
                }
            } else {
                formData.append('order', '');
            }
            
            // 处理 limit 参数
            if (data.limit !== undefined && data.limit !== '') {
                if (typeof data.limit === 'object') {
                    formData.append('limit', JSON.stringify(data.limit));
                } else {
                    formData.append('limit', data.limit.toString());
                }
            } else {
                formData.append('limit', '10');  // 默认值
            }
            
            // 处理 field 参数
            if (this.options.field) {
                if (Array.isArray(this.options.field)) {
                    formData.append('field', JSON.stringify(this.options.field));
                } else {
                    formData.append('field', this.options.field);
                }
            } else {
                formData.append('field', '');
            }
            
            // 处理 args 参数
            if (args) {
                formData.append('args', JSON.stringify(args));
            } else {
                formData.append('args', 'null');
            }
            
            // 添加完整JSON数据作为备份
            formData.append('json_data', jsonData);
            
            console.log('即将发送表单数据', [...formData.entries()].reduce((obj, [key, value]) => {
                obj[key] = value;
                return obj;
            }, {}));
            
            xhr.send(formData);
            console.log('请求已发送');
        });
    }

    select() {
        return this.executeQuery("select", null);
    }

    find(id) {
        var args = null;
        if (id) {
            args = [id];
        }
        return this.executeQuery("find", args);
    }

    count(field) {
        var args = null;
        if (field) {
            args = [field];
        }
        return this.executeQuery("count", args);
    }

    avg(field) {
        var args = null;
        if (field) {
            args = [field];
        }
        return this.executeQuery("avg", args);
    }

    max(field) {
        var args = null;
        if (field) {
            args = [field];
        }
        return this.executeQuery("max", args);
    }

    min(field) {
        var args = null;
        if (field) {
            args = [field];
        }
        return this.executeQuery("min", args);
    }

    sum(field) {
        var args = null;
        if (field) {
            args = [field];
        }
        return this.executeQuery("sum", args);
    }

    order(field, sort) {
        var len = arguments.length;
        var order = field;
        if (len == 2) {
            order += " " + sort;
        }
        this.getOptionList("order").push(order);
        return this;
    }

    limit(offset, nLimit) {
        var len = arguments.length;
        var map = this.getOptionMap("limit");
        if (len == 1) {
            // 直接设置一个简单的数字
            console.log('设置简单数值 limit:', offset);
            this.options.limit = offset;
            return this;
        }
        
        // 使用对象格式存储
        map.size = Math.floor(nLimit);
        map.offset = Math.floor(offset);
        
        // 为了兼容后端，存储为对象
        console.log('设置对象格式 limit:', map);
        this.options.limit = map;
        return this;
    }

    field(fi) {
        this.getOptionList("field").push(fi);
        return this;
    }

    getOptionMap(name) {
        if (!this.options[name]) {
            this.options[name] = {};
        }
        return this.options[name];
    }

    getOptionList(name) {
        if (!this.options[name]) {
            this.options[name] = [];
        }
        return this.options[name];
    }
}

export class QueryRef extends Query {
    constructor(name) {
        super(name);
    }

    execute(func, value, ...arg) {
        const v = ref(value);
        super[func].apply(this, arg).then(
            (res) => {
                v.value = res;
            },
            (err) => {
                console.error("获取数据出错了", err);
                v.value = value;
            }
        );
        return v;
    }

    selectRef() {
        return this.execute("select", []);
    }

    findRef(id) {
        return this.execute("find", {}, id);
    }

    sumRef(field) {
        return this.execute("sum", 0, field);
    }

    countRef(field) {
        return this.execute("count", 0, field);
    }

    minRef(field) {
        return this.execute("min", 0, field);
    }

    maxRef(field) {
        return this.execute("max", 0, field);
    }

    avgRef(field) {
        return this.execute("avg", 0, field);
    }
}

export const DB = {
    name(name) {
        return new QueryRef(name);
    },
    find(sql, binds = []) {
        const data = {
            sql,
            type: "find",
            binds,
        };
        
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            const url = config.service_url + config.select_url;
            
            console.log('DB.find 发送请求:', url, data);
            
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.withCredentials = true;
            
            xhr.onload = function() {
                console.log('DB.find 响应状态:', xhr.status);
                console.log('DB.find 响应内容:', xhr.responseText);
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        console.log('DB.find 解析后的响应:', response);
                        
                        if (response.code === 0) {
                            // 处理可能的嵌套结构
                            if (response.data && response.data.data) {
                                console.log('DB.find 返回嵌套数据:', response.data.data);
                                resolve(response.data.data);
                            } else {
                                console.log('DB.find 返回直接数据:', response.data);
                                resolve(response.data);
                            }
                        } else {
                            console.error('DB.find 服务器返回错误:', response.msg);
                            reject(new Error(response.msg || '请求失败'));
                        }
                    } catch (e) {
                        console.error('DB.find 解析响应失败:', e);
                        reject(e);
                    }
                } else {
                    console.error('DB.find 请求失败, 状态码:', xhr.status);
                    reject(new Error(`请求失败，状态码: ${xhr.status}`));
                }
            };
            
            xhr.onerror = function(e) {
                console.error('DB.find 请求错误:', e);
                reject(new Error('请求发送失败'));
            };
            
            xhr.send(JSON.stringify(data));
        });
    },
    select(sql, binds = []) {
        const data = {
            sql,
            type: "select",
            binds,
        };
        
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            const url = config.service_url + config.select_url;
            
            console.log('DB.select 发送请求:', url, data);
            
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.withCredentials = true;
            
            xhr.onload = function() {
                console.log('DB.select 响应状态:', xhr.status);
                console.log('DB.select 响应内容:', xhr.responseText);
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        console.log('DB.select 解析后的响应:', response);
                        
                        if (response.code === 0) {
                            // 处理可能的嵌套结构
                            if (response.data && response.data.data) {
                                console.log('DB.select 返回嵌套数据:', response.data.data);
                                resolve(response.data.data);
                            } else {
                                console.log('DB.select 返回直接数据:', response.data);
                                resolve(response.data);
                            }
                        } else {
                            console.error('DB.select 服务器返回错误:', response.msg);
                            reject(new Error(response.msg || '请求失败'));
                        }
                    } catch (e) {
                        console.error('DB.select 解析响应失败:', e);
                        reject(e);
                    }
                } else {
                    console.error('DB.select 请求失败, 状态码:', xhr.status);
                    reject(new Error(`请求失败，状态码: ${xhr.status}`));
                }
            };
            
            xhr.onerror = function(e) {
                console.error('DB.select 请求错误:', e);
                reject(new Error('请求发送失败'));
            };
            
            xhr.send(JSON.stringify(data));
        });
    },
};

export default DB;
