// 测试脚本：用于调试聊天消息发送问题
// 将此文件复制到项目根目录，然后在浏览器控制台中运行

(function() {
    console.log('===== 开始测试聊天消息发送 =====');
    
    // 1. 测试不同时间格式的消息发送
    async function testMessageSending() {
        // 使用FormData准备测试数据
        function prepareTestData(timeFormat) {
            const testData = new FormData();
            testData.append('neirong', '测试消息 - ' + new Date().toLocaleString());
            testData.append('fasongren', '002'); // 使用一个已知的用户ID
            testData.append('fasongshijian', timeFormat);
            testData.append('shifouzhakan', '否');
            testData.append('siliaoid', '123456'); // 使用一个较小的ID值
            
            console.log('准备发送测试数据：', {
                neirong: testData.get('neirong'),
                fasongren: testData.get('fasongren'),
                fasongshijian: testData.get('fasongshijian'),
                shifouzhakan: testData.get('shifouzhakan'),
                siliaoid: testData.get('siliaoid')
            });
            
            return testData;
        }
        
        // 测试不同的时间格式
        const timeFormats = [
            new Date().toISOString().slice(0, 19).replace('T', ' '), // 2023-05-14 21:13:34
            new Date().toLocaleString(), // 5/14/2023, 9:13:34 PM
            new Date().toLocaleDateString() + ' ' + new Date().toLocaleTimeString(), // 5/14/2023 9:13:34 PM
            new Date().getFullYear() + '-' + 
                String(new Date().getMonth() + 1).padStart(2, '0') + '-' + 
                String(new Date().getDate()).padStart(2, '0') + ' ' + 
                String(new Date().getHours()).padStart(2, '0') + ':' + 
                String(new Date().getMinutes()).padStart(2, '0') + ':' + 
                String(new Date().getSeconds()).padStart(2, '0')
        ];
        
        // 测试两个API路径
        const apiUrls = ['/api/xiaoxi/insert/', '/xiaoxi/insert/'];
        
        for (const apiUrl of apiUrls) {
            console.log(`\n测试API路径: ${apiUrl}`);
            
            for (const [index, timeFormat] of timeFormats.entries()) {
                console.log(`\n测试时间格式 #${index + 1}: ${timeFormat}`);
                const testData = prepareTestData(timeFormat);
                
                try {
                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        body: testData,
                        credentials: 'include',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });
                    
                    console.log(`响应状态: ${response.status} ${response.statusText}`);
                    
                    if (!response.ok) {
                        console.error(`服务器错误: ${response.status}`);
                        continue;
                    }
                    
                    const result = await response.json();
                    console.log('响应数据:', result);
                    
                    if (result.code === 0 || result.id) {
                        console.log('✅ 测试成功: 时间格式可以正常工作!');
                    } else {
                        console.error('❌ 测试失败:', result.msg || '未知错误');
                    }
                } catch (error) {
                    console.error('❌ 请求错误:', error);
                }
            }
        }
    }
    
    // 2. 检查rule.date函数是否正常工作
    function testRuleDateFunction() {
        console.log('\n===== 测试 rule.date 函数 =====');
        try {
            // 假设rule.date已经加载
            if (typeof rule !== 'undefined' && typeof rule.date === 'function') {
                const formattedDate = rule.date("Y-m-d H:i:s");
                console.log('rule.date 函数输出:', formattedDate);
                console.log('检查日期格式是否符合 YYYY-MM-DD HH:MM:SS:', /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(formattedDate));
            } else {
                console.error('rule.date 函数不可用，请在前端应用中运行此脚本');
            }
        } catch (error) {
            console.error('测试 rule.date 函数时出错:', error);
        }
    }
    
    // 运行测试
    testMessageSending().then(() => {
        testRuleDateFunction();
        console.log('\n===== 测试完成 =====');
    });
})(); 