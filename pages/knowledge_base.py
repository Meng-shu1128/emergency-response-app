import streamlit as st
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

KNOWLEDGE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'knowledge_base.json')

def load_knowledge_base():
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'emergency_contacts': [],
        'procedures': [],
        'resources': []
    }

def save_knowledge_base(data):
    with open(KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def show_knowledge_base():
    st.title("📚 知识库管理")
    st.markdown("---")
    
    kb = load_knowledge_base()
    
    tab1, tab2, tab3 = st.tabs(["📞 紧急联系人", "📋 应急流程", "🔗 资源链接"])
    
    with tab1:
        st.subheader("紧急联系人管理")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_contact"):
                name = st.text_input("联系人姓名", placeholder="请输入姓名")
                phone = st.text_input("联系电话", placeholder="请输入电话")
                department = st.text_input("部门/机构", placeholder="请输入部门或机构名称")
                description = st.text_area("描述", placeholder="请输入描述信息...")
                
                if st.form_submit_button("添加联系人", type="primary"):
                    if name and phone:
                        kb['emergency_contacts'].append({
                            'name': name,
                            'phone': phone,
                            'department': department,
                            'description': description
                        })
                        save_knowledge_base(kb)
                        st.success("联系人已添加！")
                        st.rerun()
                    else:
                        st.error("请填写姓名和电话！")
        
        with col2:
            st.markdown("### 现有联系人")
            for idx, contact in enumerate(kb['emergency_contacts']):
                with st.expander(f"{contact['name']} - {contact['department']}"):
                    st.write(f"**电话**: {contact['phone']}")
                    if contact['description']:
                        st.write(f"**描述**: {contact['description']}")
                    
                    if st.button("删除", key=f"del_contact_{idx}"):
                        kb['emergency_contacts'].pop(idx)
                        save_knowledge_base(kb)
                        st.rerun()
    
    with tab2:
        st.subheader("应急流程管理")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_procedure"):
                title = st.text_input("流程标题", placeholder="请输入流程标题")
                category = st.selectbox("类别", ["医疗急救", "火灾", "治安", "自然灾害", "其他"])
                steps = st.text_area("流程步骤", placeholder="每行一个步骤，例如：\n1. 拨打120\n2. 保持冷静\n3. 检查呼吸", height=150)
                
                if st.form_submit_button("添加流程", type="primary"):
                    if title and steps:
                        kb['procedures'].append({
                            'title': title,
                            'category': category,
                            'steps': [step.strip() for step in steps.split('\n') if step.strip()]
                        })
                        save_knowledge_base(kb)
                        st.success("流程已添加！")
                        st.rerun()
                    else:
                        st.error("请填写标题和步骤！")
        
        with col2:
            st.markdown("### 现有流程")
            for idx, procedure in enumerate(kb['procedures']):
                with st.expander(f"{procedure['title']} - {procedure['category']}"):
                    st.write(f"**类别**: {procedure['category']}")
                    st.write("**步骤**:")
                    for step in procedure['steps']:
                        st.write(f"- {step}")
                    
                    if st.button("删除", key=f"del_procedure_{idx}"):
                        kb['procedures'].pop(idx)
                        save_knowledge_base(kb)
                        st.rerun()
    
    with tab3:
        st.subheader("资源链接管理")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_resource"):
                title = st.text_input("资源标题", placeholder="请输入资源标题")
                url = st.text_input("链接地址", placeholder="请输入URL")
                category = st.selectbox("类别", ["官方网站", "学习资料", "视频教程", "工具下载", "其他"])
                description = st.text_area("描述", placeholder="请输入描述信息...")
                
                if st.form_submit_button("添加资源", type="primary"):
                    if title and url:
                        kb['resources'].append({
                            'title': title,
                            'url': url,
                            'category': category,
                            'description': description
                        })
                        save_knowledge_base(kb)
                        st.success("资源已添加！")
                        st.rerun()
                    else:
                        st.error("请填写标题和链接地址！")
        
        with col2:
            st.markdown("### 现有资源")
            for idx, resource in enumerate(kb['resources']):
                with st.expander(f"{resource['title']}"):
                    st.write(f"**类别**: {resource['category']}")
                    st.write(f"**链接**: {resource['url']}")
                    if resource['description']:
                        st.write(f"**描述**: {resource['description']}")
                    
                    if st.button("删除", key=f"del_resource_{idx}"):
                        kb['resources'].pop(idx)
                        save_knowledge_base(kb)
                        st.rerun()
