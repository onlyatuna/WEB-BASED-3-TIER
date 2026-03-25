import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { ItemService } from './item.service';

@Controller('item')
export class ItemController {
  constructor(private readonly svc: ItemService) {}

  @Get()
  findAll() { return this.svc.findAll(); }

  @Post()
  create(@Body() b: { item_code: string; item_name: string; fact_code: string }) {
    return this.svc.create(b.item_code, b.item_name, b.fact_code);
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() b: { item_name: string; fact_code: string }) {
    return this.svc.update(id, b.item_name, b.fact_code);
  }

  @Delete(':id')
  remove(@Param('id') id: string) { return this.svc.remove(id); }
}
