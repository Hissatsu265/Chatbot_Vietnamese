document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const uploadBox = document.getElementById('upload-box');
    const fileUpload = document.getElementById('file-upload');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const processBtn = document.getElementById('process-btn');
    const chatContainer = document.getElementById('chat-container');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const newChatBtn = document.getElementById('new-chat-btn');

    // Upload box click event
    uploadBox.addEventListener('click', function() {
        fileUpload.click();
    });

    // File upload change event
    fileUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            
            // Check if file is PDF
            if (file.type !== 'application/pdf') {
                alert('Vui lòng chọn file PDF.');
                return;
            }
            
            // Display file info
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            uploadBox.classList.add('hidden');
            fileInfo.classList.remove('hidden');
        }
    });

    // Process button click event
    processBtn.addEventListener('click', function() {
        // Simulate processing time
        processBtn.disabled = true;
        processBtn.textContent = 'Đang xử lý...';
        
        setTimeout(function() {
            fileInfo.classList.add('hidden');
            chatContainer.classList.remove('hidden');
            processBtn.disabled = false;
            processBtn.textContent = 'Xử lý tài liệu';
            
            // Scroll to the bottom of chat messages
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 2000);
    });

    // Send button click event
    sendBtn.addEventListener('click', sendMessage);

    // User input keypress event
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // New chat button click event
    newChatBtn.addEventListener('click', function() {
        // Reset the chat
        chatContainer.classList.add('hidden');
        uploadBox.classList.remove('hidden');
        fileUpload.value = '';
        userInput.value = '';
        
        // Clear previous chat except the first bot message
        while (chatMessages.children.length > 1) {
            chatMessages.removeChild(chatMessages.lastChild);
        }
    });

    // Drag and drop functionality
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', function() {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            if (file.type !== 'application/pdf') {
                alert('Vui lòng chọn file PDF.');
                return;
            }
            
            // Update file input
            fileUpload.files = e.dataTransfer.files;
            
            // Display file info
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            uploadBox.classList.add('hidden');
            fileInfo.classList.remove('hidden');
        }
    });

    // Function to send message
    function sendMessage() {
        const message = userInput.value.trim();
        if (message !== '') {
            // Add user message
            addMessage('user', message);
            
            // Clear input
            userInput.value = '';
            
            // Simulate bot response after a short delay
            setTimeout(function() {
                generateBotResponse(message);
            }, 1000);
        }
    }

    // Function to add message to chat
    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'avatar';
        
        const icon = document.createElement('i');
        icon.className = type === 'user' ? 'fas fa-user' : 'fas fa-robot';
        avatarDiv.appendChild(icon);
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';
        
        const paragraph = document.createElement('p');
        paragraph.textContent = content;
        contentDiv.appendChild(paragraph);
        
        if (type === 'user') {
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(avatarDiv);
        } else {
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(contentDiv);
        }
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of chat messages
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to generate bot response based on user input
    function generateBotResponse(userMessage) {
        let response;
        
        // Simple responses based on common questions
        if (userMessage.toLowerCase().includes('tóm tắt') || userMessage.toLowerCase().includes('summary')) {
            response = `Dựa trên tài liệu của bạn, tôi có thể tóm tắt nội dung chính như sau:
            
Tài liệu này tập trung vào [chủ đề chính] và trình bày những phân tích quan trọng về [lĩnh vực]. Phần đầu giới thiệu tổng quan về [bối cảnh], tiếp theo là phân tích chi tiết về [các yếu tố quan trọng]. Cuối cùng, tài liệu đưa ra các kết luận và đề xuất về [hướng phát triển/giải pháp].

Điểm nổi bật của tài liệu là phân tích về [điểm nhấn] và đề xuất [giải pháp sáng tạo] để giải quyết [vấn đề].`;
        }
        else if (userMessage.toLowerCase().includes('kết luận') || userMessage.toLowerCase().includes('conclusion')) {
            response = `Phần kết luận của tài liệu nhấn mạnh những điểm sau:

1. [Kết luận chính 1] đã được chứng minh qua các số liệu và phân tích.
2. [Kết luận chính 2] được khuyến nghị áp dụng trong [ngữ cảnh cụ thể].
3. Những hạn chế hiện tại bao gồm [hạn chế 1] và [hạn chế 2].
4. Hướng phát triển trong tương lai nên tập trung vào [hướng phát triển].

Tác giả kết thúc bằng việc nhấn mạnh tầm quan trọng của [yếu tố then chốt] trong việc thúc đẩy [mục tiêu cuối cùng].`;
        }
        else if (userMessage.toLowerCase().includes('phần 1') || userMessage.toLowerCase().includes('giới thiệu')) {
            response = `Phần 1 của tài liệu giới thiệu về [chủ đề] với những nội dung chính sau:

- Bối cảnh và tầm quan trọng của [chủ đề] trong [lĩnh vực/ngành].
- Tổng quan về tình hình nghiên cứu hiện tại liên quan đến [chủ đề].
- Những thách thức chính đang đối mặt trong việc [mục tiêu/vấn đề].
- Mục tiêu và phạm vi của nghiên cứu/tài liệu này.

Tác giả đặc biệt nhấn mạnh sự cần thiết của [yếu tố] trong bối cảnh [xu hướng hiện tại].`;
        }
        else if (userMessage.toLowerCase().includes('phần 2') || userMessage.toLowerCase().includes('phân tích')) {
            response = `Phần 2 của tài liệu tập trung vào phân tích chi tiết với những nội dung sau:

- Phương pháp tiếp cận và thu thập dữ liệu về [chủ đề].
- Phân tích các yếu tố chính bao gồm [yếu tố 1], [yếu tố 2] và [yếu tố 3].
- Mối quan hệ giữa [yếu tố X] và [kết quả Y] được chứng minh qua [phương pháp/mô hình].
- Kết quả phân tích cho thấy [phát hiện quan trọng 1] và [phát hiện quan trọng 2].

Các bảng dữ liệu và biểu đồ trong phần này minh họa rõ ràng sự tương quan giữa [biến số] và tác động của chúng đến [kết quả].`;
        }
        else if (userMessage.toLowerCase().includes('phần 3') || userMessage.toLowerCase().includes('giải pháp')) {
            response = `Phần 3 của tài liệu đề xuất các giải pháp và kết luận:

- Giải pháp 1: [Mô tả giải pháp] được đề xuất để giải quyết [vấn đề cụ thể].
- Giải pháp 2: Áp dụng [phương pháp/công nghệ] để nâng cao hiệu quả của [quy trình/hệ thống].
- Khuyến nghị về việc triển khai [chiến lược] trong [bối cảnh cụ thể].
- Đánh giá tính khả thi và những hạn chế tiềm ẩn của các giải pháp đề xuất.

Tác giả cũng đưa ra lộ trình thực hiện với các mốc thời gian cụ thể và phương pháp đánh giá hiệu quả.`;
        }
        else {
            response = `Dựa trên tài liệu của bạn, tôi có thể trả lời rằng:

Nội dung bạn hỏi về "${userMessage}" được đề cập trong tài liệu ở [phần/trang] với những điểm chính sau:

1. [Điểm chính 1] liên quan đến câu hỏi của bạn.
2. [Điểm chính 2] bổ sung thêm thông tin về chủ đề này.
3. Tài liệu cũng đề cập đến [thông tin liên quan] có thể giúp bạn hiểu rõ hơn.

Bạn có muốn tôi cung cấp thêm thông tin chi tiết về điểm nào không?`;
        }
        
        // Add complex HTML response with formatting for the bot
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'avatar';
        
        const icon = document.createElement('i');
        icon.className = 'fas fa-robot';
        avatarDiv.appendChild(icon);
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';
        
        // Process response with simple formatting
        const paragraphs = response.split('\n\n');
        paragraphs.forEach(paragraph => {
            if (paragraph.trim() !== '') {
                if (paragraph.includes('- ')) {
                    // Create unordered list
                    const ul = document.createElement('ul');
                    const items = paragraph.split('- ');
                    
                    items.forEach((item, index) => {
                        if (item.trim() !== '' && index > 0) {
                            const li = document.createElement('li');
                            li.textContent = item.trim();
                            ul.appendChild(li);
                        }
                    });
                    
                    contentDiv.appendChild(ul);
                } else if (paragraph.match(/^\d+\./)) {
                    // Create ordered list
                    const ol = document.createElement('ol');
                    const items = paragraph.split(/\d+\.\s+/);
                    
                    items.forEach((item, index) => {
                        if (item.trim() !== '' && index > 0) {
                            const li = document.createElement('li');
                            li.textContent = item.trim();
                            ol.appendChild(li);
                        }
                    });
                    
                    contentDiv.appendChild(ol);
                } else {
                    // Create regular paragraph
                    const p = document.createElement('p');
                    p.textContent = paragraph.trim();
                    contentDiv.appendChild(p);
                }
            }
        });
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of chat messages
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        
        return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Auto resize textarea as user types
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        
        // Reset height if no content
        if (this.value === '') {
            this.style.height = 'auto';
        }
    });

    // Add additional chat interactions
    const chatExamples = [
        {
            question: "Có những khái niệm chính nào trong tài liệu này?",
            answer: `Dựa trên nội dung tài liệu, những khái niệm chính bao gồm:

1. <strong>Khái niệm A:</strong> Được định nghĩa là [định nghĩa] và đóng vai trò quan trọng trong [bối cảnh].

2. <strong>Khái niệm B:</strong> Liên quan đến [lĩnh vực] và thường được sử dụng khi [tình huống].

3. <strong>Khái niệm C:</strong> Một cách tiếp cận mới để giải quyết [vấn đề] với những ưu điểm như [ưu điểm].

4. <strong>Khái niệm D:</strong> Mô hình tổng hợp từ [nguồn] và được áp dụng trong [trường hợp].

Các khái niệm này được phân tích chi tiết trong phần [X] của tài liệu và có mối liên hệ chặt chẽ với nhau trong việc giải quyết [vấn đề chính].`
        },
        {
            question: "So sánh phương pháp X và Y trong tài liệu",
            answer: `Tài liệu có so sánh chi tiết giữa phương pháp X và Y với những điểm sau:

<strong>Phương pháp X:</strong>
- Ưu điểm: Hiệu quả cao trong [tình huống 1], tiết kiệm [nguồn lực], dễ triển khai
- Hạn chế: Không phù hợp với [điều kiện], cần nhiều [yêu cầu đặc biệt]
- Phạm vi áp dụng: Phù hợp với [môi trường/ngữ cảnh]

<strong>Phương pháp Y:</strong>
- Ưu điểm: Linh hoạt trong [tình huống 2], kết quả ổn định, ít tốn [nguồn lực]
- Hạn chế: Phức tạp hơn trong triển khai, thời gian thực hiện lâu hơn
- Phạm vi áp dụng: Tối ưu cho [môi trường/ngữ cảnh]

Theo phân tích trong tài liệu, phương pháp X phù hợp hơn cho [tình huống A] trong khi phương pháp Y được khuyến nghị cho [tình huống B]. Trang [số trang] có bảng so sánh chi tiết các thông số kỹ thuật của hai phương pháp.`
        }
    ];

    // Function to add example chat buttons
    function addExampleChatButtons() {
        const exampleButtonsDiv = document.createElement('div');
        exampleButtonsDiv.className = 'example-buttons';
        exampleButtonsDiv.style.display = 'flex';
        exampleButtonsDiv.style.flexWrap = 'wrap';
        exampleButtonsDiv.style.gap = '10px';
        exampleButtonsDiv.style.marginTop = '20px';
        exampleButtonsDiv.style.justifyContent = 'center';
        
        chatExamples.forEach(example => {
            const button = document.createElement('button');
            button.textContent = example.question;
            button.style.padding = '8px 16px';
            button.style.backgroundColor = '#e2e8f0';
            button.style.border = 'none';
            button.style.borderRadius = '16px';
            button.style.cursor = 'pointer';
            button.style.transition = 'all 0.3s ease';
            
            button.addEventListener('mouseover', function() {
                this.style.backgroundColor = '#cbd5e1';
            });
            
            button.addEventListener('mouseout', function() {
                this.style.backgroundColor = '#e2e8f0';
            });
            
            button.addEventListener('click', function() {
                // Add user message
                addMessage('user', example.question);
                
                // Add bot response after a short delay
                setTimeout(function() {
                    // Add complex HTML response with formatting for the bot
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message bot';
                    
                    const avatarDiv = document.createElement('div');
                    avatarDiv.className = 'avatar';
                    
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-robot';
                    avatarDiv.appendChild(icon);
                    
                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'content';
                    contentDiv.innerHTML = example.answer;
                    
                    messageDiv.appendChild(avatarDiv);
                    messageDiv.appendChild(contentDiv);
                    
                    chatMessages.appendChild(messageDiv);
                    
                    // Scroll to the bottom of chat messages
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    
                    // Remove example buttons after selection
                    exampleButtonsDiv.remove();
                }, 1000);
            });
            
            exampleButtonsDiv.appendChild(button);
        });
        
        // Add to the first bot message
        if (chatMessages.firstChild) {
            chatMessages.firstChild.querySelector('.content').appendChild(exampleButtonsDiv);
        }
    }

    // Add extra features for better user experience
    function enhanceUserExperience() {
        // Add loading animation for bot responses
        const originalSendMessage = sendMessage;
        sendMessage = function() {
            const message = userInput.value.trim();
            if (message !== '') {
                // Add user message
                addMessage('user', message);
                
                // Clear input
                userInput.value = '';
                userInput.style.height = 'auto';
                
                // Add typing indicator
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message bot typing';
                
                const avatarDiv = document.createElement('div');
                avatarDiv.className = 'avatar';
                
                const icon = document.createElement('i');
                icon.className = 'fas fa-robot';
                avatarDiv.appendChild(icon);
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'content';
                
                const typingIndicator = document.createElement('div');
                typingIndicator.className = 'typing-indicator';
                typingIndicator.innerHTML = '<span></span><span></span><span></span>';
                
                contentDiv.appendChild(typingIndicator);
                typingDiv.appendChild(avatarDiv);
                typingDiv.appendChild(contentDiv);
                
                chatMessages.appendChild(typingDiv);
                
                // Scroll to the bottom of chat messages
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                // Simulate bot response after a short delay
                setTimeout(function() {
                    // Remove typing indicator
                    chatMessages.removeChild(typingDiv);
                    
                    // Generate response
                    generateBotResponse(message);
                }, 1500);
            }
        };
        
        // Add CSS for typing indicator
        const style = document.createElement('style');
        style.textContent = `
            .typing-indicator {
                display: flex;
                align-items: center;
            }
            
            .typing-indicator span {
                height: 8px;
                width: 8px;
                margin: 0 2px;
                background-color: var(--dark-gray);
                border-radius: 50%;
                display: inline-block;
                animation: bounce 1.5s infinite ease-in-out;
            }
            
            .typing-indicator span:nth-child(1) {
                animation-delay: 0s;
            }
            
            .typing-indicator span:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-indicator span:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes bounce {
                0%, 60%, 100% {
                    transform: translateY(0);
                }
                30% {
                    transform: translateY(-6px);
                }
            }
            
            .upload-box.dragover {
                border-color: var(--primary-color);
                background-color: rgba(37, 99, 235, 0.05);
            }
            
            .example-buttons button:hover {
                background-color: var(--primary-light) !important;
                color: white;
            }
        `;
        document.head.appendChild(style);
    }

    // Initialize advanced features
    enhanceUserExperience();
    
    // Add example chat buttons after a short delay
    setTimeout(addExampleChatButtons, 500);
});