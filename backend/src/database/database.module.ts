import { Global, Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as sql from 'mssql';

@Global()
@Module({
  providers: [
    {
      provide: 'MSSQL_POOL',
      useFactory: async (cfg: ConfigService): Promise<sql.ConnectionPool> => {
        const pool = new sql.ConnectionPool({
          server:   cfg.get<string>('DB_SERVER'),
          port:     parseInt(cfg.get<string>('DB_PORT'), 10),
          database: cfg.get<string>('DB_DATABASE'),
          user:     cfg.get<string>('DB_USER'),
          password: cfg.get<string>('DB_PASSWORD'),
          options:  { trustServerCertificate: true },
        });
        return pool.connect();
      },
      inject: [ConfigService],
    },
  ],
  exports: ['MSSQL_POOL'],
})
export class DatabaseModule {}
