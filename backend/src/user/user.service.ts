import { Injectable, Inject } from '@nestjs/common';
import * as sql from 'mssql';

@Injectable()
export class UserService {
  constructor(@Inject('MSSQL_POOL') private pool: sql.ConnectionPool) {}

  async findAll() {
    const res = await this.pool.request()
      .query('SELECT userid, username, pwd FROM [user]');
    return res.recordset;
  }

  async create(userid: string, username: string, pwd: string) {
    await this.pool.request()
      .input('userid',   sql.NVarChar, userid)
      .input('username', sql.NVarChar, username)
      .input('pwd',      sql.NVarChar, pwd)
      .query('INSERT INTO [user](userid, username, pwd) VALUES(@userid, @username, @pwd)');
  }

  async update(userid: string, username: string, pwd: string) {
    await this.pool.request()
      .input('username', sql.NVarChar, username)
      .input('pwd',      sql.NVarChar, pwd)
      .input('userid',   sql.NVarChar, userid)
      .query('UPDATE [user] SET username=@username, pwd=@pwd WHERE userid=@userid');
  }

  async remove(userid: string) {
    await this.pool.request()
      .input('userid', sql.NVarChar, userid)
      .query('DELETE FROM [user] WHERE userid=@userid');
  }
}
