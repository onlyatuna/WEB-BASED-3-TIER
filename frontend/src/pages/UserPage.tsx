import React, { useEffect, useState } from 'react';
import { Button, Form, Input, message, Modal, Popconfirm, Space, Table, Typography } from 'antd';
import { ArrowLeftOutlined, PlusOutlined } from '@ant-design/icons';
import { userApi } from '../api';

interface User { userid: string; username: string; pwd: string; }

const UserPage: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [data, setData]         = useState<User[]>([]);
  const [loading, setLoading]   = useState(false);
  const [open, setOpen]         = useState(false);
  const [editing, setEditing]   = useState<User | null>(null);
  const [form]                  = Form.useForm();

  const load = async () => {
    setLoading(true);
    setData(await userApi.getAll());
    setLoading(false);
  };
  useEffect(() => { load(); }, []);

  const openAdd = () => { setEditing(null); form.resetFields(); setOpen(true); };
  const openEdit = (r: User) => { setEditing(r); form.setFieldsValue(r); setOpen(true); };

  const handleOk = async () => {
    const v = await form.validateFields();
    try {
      if (editing) {
        await userApi.update(editing.userid, { username: v.username, pwd: v.pwd });
        message.success('修改成功');
      } else {
        await userApi.create(v);
        message.success('新增成功');
      }
      setOpen(false);
      load();
    } catch (e: any) {
      message.error(e?.response?.data?.message ?? '操作失敗');
    }
  };

  const handleDelete = async (id: string) => {
    await userApi.remove(id);
    message.success('刪除成功');
    load();
  };

  const columns = [
    { title: '用戶代碼', dataIndex: 'userid',   width: 140 },
    { title: '用戶名稱', dataIndex: 'username',  width: 160 },
    { title: '用戶密碼', dataIndex: 'pwd' },
    {
      title: '操作', width: 140,
      render: (_: any, r: User) => (
        <Space>
          <Button size="small" onClick={() => openEdit(r)}>修改</Button>
          <Popconfirm title="確認刪除?" onConfirm={() => handleDelete(r.userid)}>
            <Button size="small" danger>刪除</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 16, maxWidth: 860, margin: '0 auto' }}>
      <Space style={{ marginBottom: 16 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={onBack}>返回</Button>
        <Typography.Title level={4} style={{ margin: 0 }}>USER 用戶資料維護</Typography.Title>
      </Space>
      <Button type="primary" icon={<PlusOutlined />} onClick={openAdd} style={{ marginBottom: 12 }}>新增</Button>
      <Table dataSource={data} columns={columns} rowKey="userid" loading={loading} scroll={{ x: true }} />

      <Modal
        title={editing ? '修改用戶' : '新增用戶'}
        open={open}
        onOk={handleOk}
        onCancel={() => setOpen(false)}
        okText={editing ? '修改' : '新增'}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="userid" label="用戶代碼" rules={[{ required: true, message: '必填' }]}>
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item name="username" label="用戶名稱" rules={[{ required: true, message: '必填' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="pwd" label="用戶密碼" rules={[{ required: true, message: '必填' }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default UserPage;
