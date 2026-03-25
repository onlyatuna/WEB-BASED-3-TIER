import React, { useEffect, useState } from 'react';
import { Button, Form, Input, message, Modal, Popconfirm, Space, Table, Typography } from 'antd';
import { ArrowLeftOutlined, PlusOutlined } from '@ant-design/icons';
import { custApi } from '../api';

interface Cust { cust_code: string; cust_name: string; remark: string; }

const CustPage: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [data, setData]       = useState<Cust[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen]       = useState(false);
  const [editing, setEditing] = useState<Cust | null>(null);
  const [form]                = Form.useForm();

  const load = async () => { setLoading(true); setData(await custApi.getAll()); setLoading(false); };
  useEffect(() => { load(); }, []);

  const openAdd  = () => { setEditing(null); form.resetFields(); setOpen(true); };
  const openEdit = (r: Cust) => { setEditing(r); form.setFieldsValue(r); setOpen(true); };

  const handleOk = async () => {
    const v = await form.validateFields();
    try {
      if (editing) {
        await custApi.update(editing.cust_code, { cust_name: v.cust_name, remark: v.remark });
        message.success('修改成功');
      } else {
        await custApi.create(v);
        message.success('新增成功');
      }
      setOpen(false); load();
    } catch (e: any) { message.error(e?.response?.data?.message ?? '操作失敗'); }
  };

  const handleDelete = async (id: string) => {
    await custApi.remove(id); message.success('刪除成功'); load();
  };

  const columns = [
    { title: '客戶代碼', dataIndex: 'cust_code', width: 140 },
    { title: '客戶名稱', dataIndex: 'cust_name', width: 180 },
    { title: '備註說明', dataIndex: 'remark' },
    {
      title: '操作', width: 140,
      render: (_: any, r: Cust) => (
        <Space>
          <Button size="small" onClick={() => openEdit(r)}>修改</Button>
          <Popconfirm title="確認刪除?" onConfirm={() => handleDelete(r.cust_code)}>
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
        <Typography.Title level={4} style={{ margin: 0 }}>CUST 客戶資料維護</Typography.Title>
      </Space>
      <Button type="primary" icon={<PlusOutlined />} onClick={openAdd} style={{ marginBottom: 12 }}>新增</Button>
      <Table dataSource={data} columns={columns} rowKey="cust_code" loading={loading} scroll={{ x: true }} />

      <Modal
        title={editing ? '修改客戶' : '新增客戶'}
        open={open} onOk={handleOk} onCancel={() => setOpen(false)}
        okText={editing ? '修改' : '新增'}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="cust_code" label="客戶代碼" rules={[{ required: true, message: '必填' }]}>
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item name="cust_name" label="客戶名稱" rules={[{ required: true, message: '必填' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="remark" label="備註說明">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CustPage;
