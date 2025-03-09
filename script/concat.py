import json
import os


def replace_failed_records(source_file, fixed_file, output_file):
    """
    将修复后的记录替换到源文件中的错误记录，并生成新的文件

    参数：
    source_file (str): 包含错误记录的原始文件路径
    fixed_file (str): 包含修复记录的文件路径
    output_file (str): 输出文件路径
    """
    # 读取修复后的记录，并建立id到记录的映射
    fixed_records = {}
    with open(fixed_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                if 'id' in record:
                    fixed_records[record['id']] = record
            except json.JSONDecodeError:
                print(f"警告：修复文件中有无效JSON行: {line}")

    print(f"从{fixed_file}加载了{len(fixed_records)}条修复记录")

    # 遍历原始文件，用修复的记录替换错误的记录
    count_replaced = 0
    count_preserved = 0

    with open(source_file, 'r', encoding='utf-8') as f_in:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for line in f_in:
                try:
                    record = json.loads(line.strip())

                    # 判断是否为错误记录
                    is_error = False
                    if 'reason' in record and '处理错误' in record.get('reason', ''):
                        is_error = True
                    elif 'diseases' in record and record.get('diseases') == '处理失败':
                        is_error = True

                    # 如果是错误记录且有对应的修复记录，则替换
                    if is_error and record['id'] in fixed_records:
                        f_out.write(json.dumps(fixed_records[record['id']], ensure_ascii=False) + '\n')
                        count_replaced += 1
                    else:
                        # 否则保留原记录
                        f_out.write(line)
                        count_preserved += 1

                except json.JSONDecodeError:
                    print(f"警告：源文件中有无效JSON行: {line}")
                    # 对于无法解析的行，直接写入输出文件
                    f_out.write(line)
                    count_preserved += 1

    print(f"处理完成！替换了{count_replaced}条记录，保留了{count_preserved}条记录")
    print(f"结果已保存到 {output_file}")


if __name__ == "__main__":
    source_file = "data/results_debug.jsonl"
    fixed_file = "data/result_failed_records_source.jsonl"
    output_file = "data/baseline_results.jsonl"

    replace_failed_records(source_file, fixed_file, output_file)