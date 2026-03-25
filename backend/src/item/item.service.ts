import { Injectable, Inject } from '@nestjs/common';
import * as sql from 'mssql';

@Injectable()
export class ItemService {
  constructor(@Inject('MSSQL_POOL') private pool: sql.ConnectionPool) {}

  async findAll() {
    const res = await this.pool.request().query(`
      SELECT i.item_code, i.item_name, i.fact_code, f.fact_name
      FROM item i
      LEFT JOIN fact f ON i.fact_code = f.fact_code
    `);
    return res.recordset;
  }

  async create(item_code: string, item_name: string, fact_code: string) {
    await this.pool.request()
      .input('item_code', sql.NVarChar, item_code)
      .input('item_name', sql.NVarChar, item_name)
      .input('fact_code', sql.NVarChar, fact_code)
      .query('INSERT INTO item(item_code, item_name, fact_code) VALUES(@item_code, @item_name, @fact_code)');
  }

  async update(item_code: string, item_name: string, fact_code: string) {
    await this.pool.request()
      .input('item_name', sql.NVarChar, item_name)
      .input('fact_code', sql.NVarChar, fact_code)
      .input('item_code', sql.NVarChar, item_code)
      .query('UPDATE item SET item_name=@item_name, fact_code=@fact_code WHERE item_code=@item_code');
  }

  async remove(item_code: string) {
    await this.pool.request()
      .input('item_code', sql.NVarChar, item_code)
      .query('DELETE FROM item WHERE item_code=@item_code');
  }
}
