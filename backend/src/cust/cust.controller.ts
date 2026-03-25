import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { CustService } from './cust.service';

@Controller('cust')
export class CustController {
  constructor(private readonly svc: CustService) {}

  @Get()
  findAll() { return this.svc.findAll(); }

  @Post()
  create(@Body() b: { cust_code: string; cust_name: string; remark: string }) {
    return this.svc.create(b.cust_code, b.cust_name, b.remark);
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() b: { cust_name: string; remark: string }) {
    return this.svc.update(id, b.cust_name, b.remark);
  }

  @Delete(':id')
  remove(@Param('id') id: string) { return this.svc.remove(id); }
}
