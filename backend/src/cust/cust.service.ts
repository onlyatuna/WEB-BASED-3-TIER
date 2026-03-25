import { Injectable, Inject } from '@nestjs/common';
import * as sql from 'mssql';

@Injectable()
export class CustService {
  constructor(@Inject('MSSQL_POOL') private pool: sql.ConnectionPool) {}

  async findAll() {
    const res = await this.pool.request()
      .query('SELECT cust_code, cust_name, remark FROM cust');
    return res.recordset;
  }

  async create(cust_code: string, cust_name: string, remark: string) {
    await this.pool.request()
      .input('cust_code', sql.NVarChar, cust_code)
      .input('cust_name', sql.NVarChar, cust_name)
      .input('remark',    sql.NVarChar, remark)
      .query('INSERT INTO cust(cust_code, cust_name, remark) VALUES(@cust_code, @cust_name, @remark)');
  }

  async update(cust_code: string, cust_name: string, remark: string) {
    await this.pool.request()
      .input('cust_name', sql.NVarChar, cust_name)
      .input('remark',    sql.NVarChar, remark)
      .input('cust_code', sql.NVarChar, cust_code)
      .query('UPDATE cust SET cust_name=@cust_name, remark=@remark WHERE cust_code=@cust_code');
  }

  async remove(cust_code: string) {
    await this.pool.request()
      .input('cust_code', sql.NVarChar, cust_code)
      .query('DELETE FROM cust WHERE cust_code=@cust_code');
  }
}
