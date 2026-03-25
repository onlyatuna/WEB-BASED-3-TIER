import { Module } from '@nestjs/common';
import { CustController } from './cust.controller';
import { CustService } from './cust.service';

@Module({ controllers: [CustController], providers: [CustService] })
export class CustModule {}
