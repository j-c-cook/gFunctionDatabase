# Jack C. Cook
# 7/1/20

# use an excel file to create many rectangular fields

import Create_Rectangular_Fields as fieldgen


def main():

    path = 'create_w_batch.xlsx'
    fieldgen.Batch_Gen.BatchProcess(path, output_path='OutputFolder')


if __name__ == '__main__':
    main()
