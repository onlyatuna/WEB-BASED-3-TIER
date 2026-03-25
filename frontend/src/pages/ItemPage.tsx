import React, { useEffect, useState } from 'react';
import { Button, Form, Input, message, Modal, Popconfirm, Select, Space, Table, Typography } from 'antd';
import { ArrowLeftOutlined, PlusOutlined } from '@ant-design/icons';
import { itemApi, factApi } from '../api';

interface Item { item_code: string; item_name: string; fact_code: string; fact_name?: string; }
interface FactOption { fact_code: string; fact_name: string; }

const ItemPage: React.FC<{ onBack: () => void }> = ({ onBack }) => {
  const [data, setData]             = useState<Item[]>([]);
  const [factOpts, setFactOpts]     = useState<FactOption[]>([]);
  const [loading, setLoading]       = useState(false);
  const [open, setOpen]             = useState(false);
  const [editing, setEditing]       = useState<Item | null>(null);
  const [form]                      = Form.useForm();

  const load = async () => {
    setLoading(true);
    const [items, facts] = await Promise.all([itemApi.getAll(), factApi.getAll()]);
    setData(items);
    setFactOpts(facts);
    setLoading(false);
  };
  useEffect(() => { load(); }, []);

  const openAdd  = () => { setEditing(null); form.resetFields(); setOpen(true); };
  const openEdit = (r: Item) => { setEditing(r); form.setFieldsValue(r); setOpen(true); };

  const handleOk = async () => {
    const v = await form.validateFields();
    try {
      if (editing) {
        await itemApi.update(editing.item_code, { item_name: v.item_name, fact_code: v.fact_code });
        message.success('修改成功');
      } else {
        await itemApi.create(v);
        message.success('新增成功');
      }
      setOpen(false); load();
    } catch (e: any) { message.error(e?.response?.data?.message ?? '操作失敗'); }
  };

  const handleDelete = async (id: string) => {
    await itemApi.remove(id); message.success('刪除成功'); load();
  };

  const columns = [
    { title: '商品代碼', dataIndex: 'item_code', width: 140 },
    { title: '商品名稱', dataIndex: 'item_name', width: 180 },
    { title: '主供應商代碼', dataIndex: 'fact_code', width: 130 },
    { title: '主供應商名稱', dataIndex: 'fact_name' },
    {
      title: '操作', width: 140,
      render: (_: any, r: Item) => (
        <Space>
          <Button size="small" onClick={() => openEdit(r)}>修改</Button>
          <Popconfirm title="確認刪除?" onConfirm={() => handleDelete(r.item_code)}>
            <Button size="small" danger>刪除</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 16, maxWidth: 900, margin: '0 auto' }}>
      <Space style={{ marginBottom: 16 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={onBack}>返回</Button>
        <Typography.Title level={4} style={{ margin: 0 }}>ITEM 商品資料維護</Typography.Title>
      </Space>
      <Button type="primary" icon={<PlusOutlined />} onClick={openAdd} style={{ marginBottom: 12 }}>新增</Button>
      <Table dataSource={data} columns={columns} rowKey="item_code" loading={loading} scroll={{ x: true }} />

      <Modal
        title={editing ? '修改商品' : '新增商品'}
        open={open} onOk={handleOk} onCancel={() => setOpen(false)}
        okText={editing ? '修改' : '新增'}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="item_code" label="商品代碼" rules={[{ required: true, message: '必填' }]}>
            <Input disabled={!!editing} />
          </Form.Item>
          <Form.Item name="item_name" label="商品名稱" rules={[{ required: true, message: '必填' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="fact_code" label="主供應商" rules={[{ required: true, message: '必填' }]}>
            <Select
              showSearch
              placeholder="請選擇廠商"
              optionFilterProp="label"
              options={factOpts.map(f => ({ value: f.fact_code, label: `${f.fact_code} ${f.fact_name}` }))}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ItemPage;
