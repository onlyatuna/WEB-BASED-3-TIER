import { Injectable, Inject } from '@nestjs/common';
import * as sql from 'mssql';

@Injectable()
export class FactService {
  constructor(@Inject('MSSQL_POOL') private pool: sql.ConnectionPool) {}

  async findAll() {
    const res = await this.pool.request()
      .query('SELECT fact_code, fact_name, remark FROM fact');
    return res.recordset;
  }

  async create(fact_code: string, fact_name: string, remark: string) {
    await this.pool.request()
      .input('fact_code', sql.NVarChar, fact_code)
      .input('fact_name', sql.NVarChar, fact_name)
      .input('remark',    sql.NVarChar, remark)
      .query('INSERT INTO fact(fact_code, fact_name, remark) VALUES(@fact_code, @fact_name, @remark)');
  }

  async update(fact_code: string, fact_name: string, remark: string) {
    await this.pool.request()
      .input('fact_name', sql.NVarChar, fact_name)
      .input('remark',    sql.NVarChar, remark)
      .input('fact_code', sql.NVarChar, fact_code)
      .query('UPDATE fact SET fact_name=@fact_name, remark=@remark WHERE fact_code=@fact_code');
  }

  async remove(fact_code: string) {
    await this.pool.request()
      .input('fact_code', sql.NVarChar, fact_code)
      .query('DELETE FROM fact WHERE fact_code=@fact_code');
  }
}
