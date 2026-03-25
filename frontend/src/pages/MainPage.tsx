import React from 'react';
import { Card, Col, Row, Typography } from 'antd';
import {
  UserOutlined,
  ShopOutlined,
  BankOutlined,
  AppstoreOutlined,
} from '@ant-design/icons';

const { Title } = Typography;

const MENU = [
  { key: 'user', label: 'USER\n用戶資料維護', icon: <UserOutlined style={{ fontSize: 36 }} />, color: '#1677ff' },
  { key: 'cust', label: 'CUST\n客戶資料維護', icon: <ShopOutlined  style={{ fontSize: 36 }} />, color: '#52c41a' },
  { key: 'fact', label: 'FACT\n廠商資料維護', icon: <BankOutlined  style={{ fontSize: 36 }} />, color: '#fa8c16' },
  { key: 'item', label: 'ITEM\n商品資料維護', icon: <AppstoreOutlined style={{ fontSize: 36 }} />, color: '#722ed1' },
];

interface Props {
  onNav: (page: any) => void;
}

const MainPage: React.FC<Props> = ({ onNav }) => (
  <div style={{ minHeight: '100vh', background: '#f0f2f5', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
    <Title level={2} style={{ marginBottom: 40 }}>資料維護系統</Title>
    <Row gutter={[24, 24]} justify="center" style={{ width: '100%', maxWidth: 600 }}>
      {MENU.map(m => (
        <Col xs={24} sm={12} key={m.key}>
          <Card
            hoverable
            onClick={() => onNav(m.key)}
            style={{ textAlign: 'center', borderTop: `4px solid ${m.color}`, cursor: 'pointer' }}
            styles={{ body: { padding: '32px 16px' } }}
          >
            <div style={{ color: m.color, marginBottom: 12 }}>{m.icon}</div>
            <div style={{ whiteSpace: 'pre-line', fontWeight: 600, fontSize: 16, lineHeight: 1.8 }}>{m.label}</div>
          </Card>
        </Col>
      ))}
    </Row>
  </div>
);

export default MainPage;
